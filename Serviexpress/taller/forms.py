from django.forms import ModelForm
from .models import Proveedor,FaBo,Cita,Vehiculo,Servicio,Pedido,Producto, Cliente, Empleado

class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ['desc_cita', 'cliente', 'empleado']
        
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
        fields = ['detalle_fb', 'totalpagar', 'cita']

class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente','marca','modelo','año','km','cliente']

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['cant_prod','detalle_prod','proveedor','empleado']

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['desc_prod','orden']
        
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['pnom_cli','snom_cli','appaterno_cli','apmaterno_cli','correo_cli','telefono_cli']
        
class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['pnom_emp','snom_emp','appaterno_emp','apmaterno_emp','cargo','salario']      