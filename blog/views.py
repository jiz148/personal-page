from django.shortcuts import render
from .owners import \
    OwnerListView, \
    OwnerDetailView
from .models import Article, Category


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
