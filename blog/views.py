import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .owners import \
    OwnerListView, \
    OwnerDetailView, \
    OwnerCreateView, \
    OwnerDeleteView, \
    OwnerUpdateView
from .models import Article, Category
from .forms import CreateForm


class BlogBaseView(OwnerListView):
    model = Category
    template_name = 'blog_base.html'


class ArticleListView(OwnerListView):
    model = Article

    def get_queryset(self):
        return super().get_queryset()[:10]


class CategoryDetailView(OwnerDetailView):
    model = Category


class ArticleDetailView(OwnerDetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, View):
    template_name = 'blog/article_form.html'

    # instead of redirecting, return the url as a reference
    success_url = reverse_lazy('blog:article_list')

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        print('post is', request.POST)
        print('file is', request.FILES)
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            print('lallala')
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # add owner to the model before saving
        article = form.save(commit=False)
        article.owner = self.request.user
        article.save()
        return JsonResponse({"success_url": self.success_url})


class ArticleUpdateView(OwnerUpdateView):
    model = Article


class ArticleDeleteView(OwnerDeleteView):
    model = Article
