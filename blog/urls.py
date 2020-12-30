from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogBaseView.as_view(), name='base'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/category/<int:category_id>/', views.ArticleCategoryListView.as_view(), name='article_category_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('article/<int:pk>/comment/', views.CommentCreateView.as_view(), name='article_comment_create'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='article_comment_delete'),
    path('article/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='article_favorite'),
    path('article/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='article_unfavorite'),
]
