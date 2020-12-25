from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogBaseView.as_view(), name='base'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
]
