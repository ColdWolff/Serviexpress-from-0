from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('hnf/', views.hnf, name='hnf')
]