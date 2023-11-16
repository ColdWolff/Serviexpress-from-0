from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('index/', views.index, name='index'),
    path('logout/', views.signout, name='logout'),
    
    path('servicios', views.servicios, name='servicios'),
    path('create/servicio/', views.create_servicio, name='create/servicio'),
]