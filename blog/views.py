from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.db.models import Q

from .owners import \
    OwnerListView, \
    OwnerDetailView, \
    OwnerDeleteView
from .models import Article, Category, Comment, Favorite
from .forms import ArticleForm, CommentForm

BLOG_BASE_HTML = 'blog_base.html'
ARTICLE_DETAIL_HTML = 'blog/article_detail.html'
ARTICLE_FORM_HTML = 'blog/article_form.html'
ARTICLE_LIST_HTML = 'blog/article_list.html'


class BlogBaseView(OwnerListView):
    model = Category
    template_name = BLOG_BASE_HTML


class ArticleListView(View):
    template_name = ARTICLE_LIST_HTML
    paginate_by = 10

    def get(self, request):
        search_str = request.GET.get('search', False)
        category_id = request.GET.get('category_id', -1)

        ctx = _get_article_list_ctx(request, search_str, category_id, paginate_by=self.paginate_by)

        return render(request, self.template_name, ctx)


class ArticleDetailView(OwnerDetailView):
    model = Article
    template_name = ARTICLE_DETAIL_HTML

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        # favorites
        favorites = list()
        if request.user.is_authenticated:
            favorites = _get_favorites(request)

        ctx = _get_comment_ctx(article)
        # favorites
        ctx['favorites'] = favorites

        return render(request, self.template_name, ctx)


class ArticleCreateView(LoginRequiredMixin, View):
    template_name = ARTICLE_FORM_HTML
    success_template_name = ARTICLE_LIST_HTML

    # get the url needed for form action
    form_action = reverse_lazy('blog:article_create')

    def get(self, request):
        form = ArticleForm()
        ctx = {
            'form': form,
            'form_action': self.form_action,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {
                'form': form,
                'form_action': self.form_action,
            }
            return render(request, self.template_name, ctx)

        # add owner to the model before saving
        article = form.save(commit=False)
        article.owner = self.request.user
        article.save()

        # instead of redirecting, return the article list html for front-end to generate to content
        ctx = _get_article_list_ctx(request)
        return render(request, self.success_template_name, ctx)


class ArticleUpdateView(LoginRequiredMixin, View):
    template_name = ARTICLE_FORM_HTML
    success_template_name = ARTICLE_LIST_HTML

    def get(self, request, pk):
        # get the url needed for form action
        form_action = reverse_lazy('blog:article_update', kwargs={'pk': pk})

        article = get_object_or_404(Article, pk=pk, owner=request.user)
        form = ArticleForm(instance=article)
        ctx = {
            'form': form,
            'form_action': form_action,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        # get the url needed for form action
        form_action = reverse_lazy('blog:article_update', kwargs={'pk': pk})

        article = get_object_or_404(Article, pk=pk, owner=request.user)
        form = ArticleForm(request.POST, request.FILES or None, instance=article)

        if not form.is_valid():
            ctx = {
                'form': form,
                'form_action': form_action,
            }
            return render(request, self.template_name, ctx)

        article = form.save(commit=False)
        article.save()

        # instead of redirecting, return the article list html for front-end to generate to content
        ctx = _get_article_list_ctx(request)
        return render(request, self.success_template_name, ctx)


class ArticleDeleteView(OwnerDeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, article=article)
        comment.save()

        # return the article detail page instead
        ctx = _get_comment_ctx(article)
        return render(request, ARTICLE_DETAIL_HTML, ctx)


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        article = self.object.article
        return reverse_lazy('blog:article_detail', args=[article.id])


def _get_comment_ctx(article):
    """
    Input: article
    @return:
    <Dict> ctx
    context of {'article': <Article>, 'comments': <QuerySet>, 'comment_form': <Form>}
    """
    comments = Comment.objects.filter(article=article).order_by('-updated_at')
    comment_form = CommentForm()
    ctx = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return ctx


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        fav = Favorite(owner=request.user, article=article)

        try:
            fav.save()
        # In case of duplicate key
        except IntegrityError:
            pass

        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        try:
            Favorite.objects.get(owner=request.user, article=article).delete()
        except Favorite.DoesNotExist:
            pass

        return HttpResponse()


def _get_favorites(request):
    """
    Gets the favorite articles' ids from request.user
    Input: request
    @return: <list> List of article ids
    """
    # rows = [{'id': 2}, {'id': 4} ... ]  (A list of article ids)
    rows = request.user.favorite_article.values('id')
    # favorites = [2, 4, ...] using list comprehension
    favorites = [row['id'] for row in rows]

    return favorites


def _get_article_list_ctx(request, search_str=None, category_id=-1, paginate_by=10):
    """
    Gets the context for article_list template
    @return: <dict> context of article list
    """

    # article list
    article_list = Article.objects.select_related().order_by('-updated_at')

    # multi-field search
    if search_str:
        query = Q(title__contains=search_str)
        query.add(Q(text__contains=search_str), Q.OR)
        article_list = article_list.filter(query)

    # category
    if int(category_id) >= 0:
        article_list = article_list.filter(category_id=category_id)

    # favorites
    favorites = list()
    if request.user.is_authenticated:
        favorites = _get_favorites(request)

    # paginator
    paginator = Paginator(article_list, paginate_by)  # Show paginate_by articles per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'page_obj': page_obj,
        'favorites': favorites,
        'search': search_str,
        'category_id': category_id,
    }

    return ctx
