from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cliente(models.Model):
    rut_cli = models.CharField(primary_key=True, max_length=12)
    pnom_cli = models.CharField(max_length=20)
    snom_cli = models.CharField(max_length=20, blank=True)
    appaterno_cli = models.CharField(max_length=20)
    apmaterno_cli = models.CharField(max_length=20, blank=True)
    correo_cli = models.CharField(max_length=60, blank=True)
    telefono_cli = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.pnom_cli + " " + self.appaterno_cli


class Empleado(models.Model):
    rut_emp = models.CharField(primary_key=True, max_length=12)
    pnom_emp = models.CharField(max_length=20)
    snom_emp = models.CharField(max_length=20, blank=True)
    appaterno_emp = models.CharField(max_length=20)
    apmaterno_emp = models.CharField(max_length=20, blank=True)
    cargo = models.CharField(max_length=40, blank=True)
    salario = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.pnom_emp + " " + self.appaterno_emp


class Proveedor(models.Model):
    id_prov = models.AutoField(primary_key=True)
    pnom_prov = models.CharField(max_length=20)
    snom_prov = models.CharField(max_length=20)
    appaterno_prov = models.CharField(max_length=20)
    apmaterno_prov = models.CharField(max_length=20)
    rubro = models.CharField(max_length=40)
    correo_prov = models.CharField(max_length=60)
    telefono_prov = models.IntegerField()

    def __str__(self):
        return "Proveedor: " + self.pnom_prov + " " + self.appaterno_prov


class Servicio(models.Model):
    id_serv = models.AutoField(primary_key=True)
    tipo_serv = models.CharField(max_length=50)
    desc_serv = models.TextField(max_length=400)
    costo_serv = models.IntegerField()

    def __str__(self):
        return self.tipo_serv


class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    fecha_aten = models.DateTimeField(auto_now_add=True)
    desc_cita = models.TextField(blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return "Cita N°" + str(self.id_cita) + "; Cliente:" + self.cliente.pnom_cli


class FaBo(models.Model):
    num_fb = models.AutoField(primary_key=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    detalle_fb = models.TextField()
    totalpagar = models.IntegerField()
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)

    def __str__(self):
        return "Boleta N°" + str(self.num_fb)


class Vehiculo(models.Model):
    patente = models.CharField(primary_key=True, max_length=6)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=30)
    año = models.IntegerField()
    km = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.patente)


class Pedido(models.Model):
    num_orden = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    cant_prod = models.IntegerField()
    detalle_prod = models.TextField(max_length=400)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return "N° Pedido: " + str(self.num_orden)


class Producto(models.Model):
    id_prod = models.AutoField(primary_key=True)
    desc_prod = models.TextField(max_length=400)
    orden = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    def __str__(self):
        return self.desc_prod
