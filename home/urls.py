from django.urls import path
from .views import BaseView, HomeView, EducationDetailView

app_name = 'home'

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/education/', EducationDetailView.as_view(), name='education'),
]
