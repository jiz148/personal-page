from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from .owners import \
    OwnerListView, \
    OwnerDetailView, \
    OwnerDeleteView
from .models import Article, Category
from .forms import ArticleForm

BLOG_BASE_HTML = 'blog_base.html'
ARTICLE_FORM_HTML = 'blog/article_form.html'
ARTICLE_LIST_HTML = 'blog/article_list.html'
ARTICLE_CATEGORY_LIST_HTML = 'blog/article_category_list.html'


class BlogBaseView(OwnerListView):
    model = Category
    template_name = BLOG_BASE_HTML


class ArticleListView(OwnerListView):
    model = Article

    def get_queryset(self):
        return super().get_queryset().select_related().order_by('-updated_at')[:10]


class ArticleCategoryListView(View):
    paginate_by = 10
    template_name = ARTICLE_CATEGORY_LIST_HTML

    def get(self, request, category_id):
        article_list = \
            Article.objects.select_related('category').filter(category__id=category_id).order_by('-updated_at')

        paginator = Paginator(article_list, self.paginate_by)  # Show paginate_by articles per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj})


class ArticleDetailView(OwnerDetailView):
    model = Article


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
        article_list = Article.objects.all().select_related().order_by('-updated_at')[:10]
        ctx = {'article_list': article_list}
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
        article_list = Article.objects.all().select_related().order_by('-updated_at')[:10]
        ctx = {'article_list': article_list}
        return render(request, self.success_template_name, ctx)


class ArticleDeleteView(OwnerDeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')
