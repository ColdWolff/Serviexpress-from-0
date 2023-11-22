from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Proveedor,FaBo,Cita,Vehiculo,Servicio,Pedido,Producto

class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_aten','horario', 'desc_cita', 'cliente', 'empleado']
        
    fecha_aten = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  
    )
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_aten = cleaned_data.get('fecha_aten')
        horario = cleaned_data.get('horario')

        if fecha_aten and horario:
            # Verificar si ya hay una cita para la misma fecha y hora
            citas_existente = Cita.objects.filter(fecha_aten=fecha_aten, horario=horario).exclude(id_cita=self.instance.id_cita if self.instance else None)

            if citas_existente.exists():
                raise ValidationError('Ya existe una cita agendada para la misma fecha y hora.')

        return cleaned_data

        
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