from django.urls import path
from . import views

urlpatterns = [
    #Inicio y Signs
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),

    #Cita
    path('citas', views.citas, name='citas'),
    path('create/citas/', views.create_citas, name='create_citas'),
    path('citas/<int:id_serv>/', views.update_citas, name='update_citas'),
    path('citas/<int:id_serv>/delete', views.delete_citas, name='delete_citas'),

    #Factura/Boleta
    path('fabo', views.fabo, name='fabo'),
    path('create/fabo/', views.create_fabo, name='create_fabo'),
    path('fabo/<int:id_serv>/', views.update_fabo, name='update_fabo'),
    path('fabo/<int:id_serv>/delete', views.delete_fabo, name='delete_fabo'),

    #Pedido
    path('pedidos', views.pedidos, name='pedidos'),
    path('create/pedido/', views.create_pedido, name='create_pedido'),
    path('pedido/<int:id_serv>/', views.update_pedido, name='update_pedido'),
    path('pedido/<int:id_serv>/delete', views.delete_pedido, name='delete_pedido'),

    #Producto
    path('productos', views.productos, name='productos'),
    path('create/producto/', views.create_producto, name='create_producto'),
    path('producto/<int:id_serv>/', views.update_producto, name='update_producto'),
    path('producto/<int:id_serv>/delete', views.delete_producto, name='delete_producto'),

    #Proveedor
    path('proveedores', views.proveedores, name='proveedores'),
    path('create/proveedor/', views.create_proveedor, name='create_proveedor'),
    path('proveedor/<int:id_serv>/', views.update_proveedor, name='update_proveedor'),
    path('proveedor/<int:id_serv>/delete', views.delete_proveedor, name='delete_proveedor'),

    #Servicios
    path('servicios', views.servicios, name='servicios'),
    path('create/servicio/', views.create_servicio, name='create_servicio'),
    path('servicio/<int:id_serv>/', views.update_servicio, name='update_servicio'),
    path('servicio/<int:id_serv>/delete', views.delete_servicio, name='delete_servicio'),

    #Vehiculo
    path('vehiculos', views.vehiculos, name='vehiculos'),
    path('create/vehiculo/', views.create_vehiculo, name='create_vehiculo'),
    path('vehiculo/<int:id_serv>/', views.update_vehiculo, name='update_vehiculo'),
    path('vehiculo/<int:id_serv>/delete', views.delete_vehiculo, name='delete_vehiculo'),

]