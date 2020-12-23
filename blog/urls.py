from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogBaseView.as_view(), name='base'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
]
