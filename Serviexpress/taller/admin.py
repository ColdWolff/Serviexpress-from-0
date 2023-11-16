from django.contrib import admin
from .models import Cliente, Empleado, Proveedor,FaBo,Cita,Vehiculo,Servicio,Pedido,Producto
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Proveedor)
admin.site.register(FaBo)
admin.site.register(Cita)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Pedido)
admin.site.register(Producto)