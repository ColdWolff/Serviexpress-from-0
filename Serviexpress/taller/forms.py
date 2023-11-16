from django.forms import ModelForm
from .models import Cliente, Empleado, Proveedor,FaBo,Cita,Vehiculo,Servicio,Pedido,Producto

class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ['id_cita','fecha_aten', 'desc_cita','num_fb','empleado']
        
class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['tipo_serv', 'desc_serv','costo_serv']