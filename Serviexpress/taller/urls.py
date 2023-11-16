from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    
    path('create/cita/', views.create_cita, name='create/cita'),
    #path('hnf/', views.hnf, name='hnf')
]