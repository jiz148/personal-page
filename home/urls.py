from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.BaseView.as_view(), name='base'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('home/education/', views.EducationView.as_view(), name='education'),
    path('home/experience/', views.ExperienceView.as_view(), name='experience'),
]
