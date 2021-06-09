from django.urls import path, include
from . import views


app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('<int:pk>/update', views.Update.as_view(), name='update'),
]
