from django.forms import ModelForm
from .models import Proveedor,FaBo,Cita,Vehiculo,Servicio,Pedido,Producto

class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_aten', 'desc_cita', 'cliente', 'empleado']
        
class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['tipo_serv', 'desc_serv','costo_serv']

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = ['pnom_prov', 'snom_prov', 'appaterno_prov', 'apmaterno_prov', 'rubro', 'correo_prov', 'telefono_prov']

class FaBoForm(ModelForm):
    class Meta:
        model = FaBo
        fields = ['fecha_emision', 'detalle_fb', 'totalpagar', 'cita']

class Vehiculo(ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente','marca','modelo','año','km','cliente']

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['fecha_pedido','cant_prod','detalle_prod','proveedor','empleado']

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['desc_prod','orden']