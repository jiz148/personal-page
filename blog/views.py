from django.shortcuts import render
from .owners import \
    OwnerListView, \
    OwnerDetailView, \
    OwnerCreateView, \
    OwnerDeleteView, \
    OwnerUpdateView
from .models import Article, Category
from django.urls import reverse_lazy
from django.views import View


class BlogBaseView(OwnerListView):
    model = Category
    template_name = 'blog_base.html'


class ArticleListView(OwnerListView):
    model = Article

    def get_queryset(self):
        return super().get_queryset()[:10]


class CategoryDetailView(View):
    model = Category


class ArticleDetailView(OwnerDetailView):
    model = Article


class ArticleCreateView(OwnerCreateView):
    fields = ['title', 'text', 'category', 'picture']
    model = Article
    success_url = reverse_lazy('blog:base')


class ArticleUpdateView(OwnerUpdateView):
    model = Article


class ArticleDeleteView(OwnerDeleteView):
    model = Article
