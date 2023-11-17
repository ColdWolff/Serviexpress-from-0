from django.urls import path
from . import views

urlpatterns = [
    #Inicio y Signs
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    #Servicios
    path('servicios', views.servicios, name='servicios'),
    path('create/servicio/', views.create_servicio, name='create_servicio'),
    path('servicio/<int:id_serv>/', views.update_servicio, name='update_servicio'),
]