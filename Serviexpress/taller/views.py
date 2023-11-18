from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CitaForm, ServicioForm, FaBoForm, VehiculoForm, ProveedorForm, PedidoForm, ProductoForm, ClienteForm,EmpleadoForm
from .models import (
    Cliente,
    Empleado,
    Proveedor,
    FaBo,
    Cita,
    Vehiculo,
    Servicio,
    Pedido,
    Producto,
)

def home(request):
    if request.user.is_authenticated:
        rol = ""
        try:
            cliente = Cliente.objects.get(rut_cli=request.user.username)
            rol = "Cliente"
        except Cliente.DoesNotExist:
            pass
        try:
            empleado = Empleado.objects.get(rut_emp=request.user.username)
            rol = "Empleado"
        except Empleado.DoesNotExist:
            pass
        return render(request, "home.html", {'rol': rol})
    else:
        return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signup.html")
    elif request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "signup.html", {"Mensaje": "Las contraseñas no coinciden"})
        else:
            try:
                rol = request.POST["role"]
                if request.POST["role"] == "Cliente":
                    cliente = Cliente.objects.create(
                        rut_cli=request.POST["rut"],
                        pnom_cli=request.POST["nombre"],
                        appaterno_cli=request.POST["apellido"]
                    )
                    user = User.objects.create_user(
                        username=request.POST["rut"],
                        password=request.POST["password1"]
                    )
                elif request.POST["role"] == "Empleado":
                    empleado = Empleado.objects.create(
                        rut_emp=request.POST["rut"],
                        pnom_emp=request.POST["nombre"],
                        appaterno_emp=request.POST["apellido"]
                    )
                    user = User.objects.create_user(
                        username=request.POST["rut"],
                        password=request.POST["password1"]
                    )
                login(request, user)
                return redirect("home")
            except Cliente.DoesNotExist:
                return render(request, "signup.html", {"Mensaje": "Error al crear cliente"})

    return render(request, "signup.html", {"Mensaje": "Método HTTP no permitido"})

# Detail y Update (Cliente)

def update_cli(request, username):
    cliente = Cliente.objects.filter(rut_cli=username).first()
    empleado = Empleado.objects.filter(rut_emp=username).first()
    Mensaje = ""

    if cliente:
        form = ClienteForm(instance=cliente)
        if request.method == "POST":
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                Mensaje = "Datos actualizados correctamente"

        return render(request, "perfil_cli.html", {"cliente": cliente, "form": form, "Mensaje": Mensaje})
    
    elif empleado:
        form = EmpleadoForm(instance=empleado)
        if request.method == "POST":
            form = EmpleadoForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                Mensaje = "Datos actualizados correctamente"
        
        return render(request, "perfil_emp.html", {"empleado": empleado, "form": form, "Mensaje": Mensaje})
    
    else:
        return HttpResponse("Perfil no encontrado para este usuario")
            
def signin(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signin.html")
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {"Mensaje": "Usuario o contraseña incorrectos"},
            )
        else:
            login(request, user)
            return redirect("home")


def signout(request):
    logout(request)
    return redirect("home")

def perfil_cli(request):
        return render(request, "perfil_cli.html")

def perfil_emp(request):
        return render(request, "perfil_emp.html")

# Lista todo (Servicio)
def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, "servicios.html", {"servicios": servicios})


# Crea (Servicio)
def create_servicio(request):
    if request.method == "GET":
        return render(request, "create_servicio.html", {"form": ServicioForm})
    else:
        try:
            form = ServicioForm(request.POST)
            new_servicio = form.save()
            return render(
                request,
                "create_servicio.html",
                {"Mensaje": "Servicio guardado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_servicio.html",
                {"form": ServicioForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Servicio)
def update_servicio(request, id_serv):
    if request.method == "GET":
        servicio = get_object_or_404(Servicio, pk=id_serv)
        form = ServicioForm(instance=servicio)
        return render(
            request, "detail_servicio.html", {"servicio": servicio, "form": form}
        )
    else:
        try:
            servicio = get_object_or_404(Servicio, pk=id_serv)
            form = ServicioForm(request.POST, instance=servicio)
            form.save()
            return render(
                request,
                "detail_servicio.html",
                {"Mensaje": "Servicio actualizado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_servicio.html",
                {
                    "servicio": servicio,
                    "form": form,
                    "Mensaje": "ERROR actualizando el servicio",
                },
            )

def delete_servicio(request, id_serv):
    servicio = get_object_or_404(Servicio, pk=id_serv)
    if request.method == 'POST':
            servicio.delete()
            return render(
                request,
                "detail_servicio.html",
                {"Mensaje": "Servicio eliminado exitosamente"})

# Citas
# Lista todo (Cita)
def citas(request):
    citas = Cita.objects.all()
    return render(request, "citas.html", {"citas": citas})


# Crea (Cita)
def create_cita(request):
    if request.method == "GET":
        return render(request, "create_cita.html", {"form": CitaForm})
    else:
        try:
            form = CitaForm(request.POST)
            new_cita = form.save()
            return render(
                request,
                "create_cita.html",
                {"Mensaje": "Cita guardada exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_cita.html",
                {"form": CitaForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Cita)
def update_cita(request, id_cita):
    if request.method == "GET":
        cita = get_object_or_404(Cita, pk=id_cita)
        form = CitaForm(instance=cita)
        return render(
            request, "detail_cita.html", {"cita": cita, "form": form}
        )
    else:
        try:
            cita = get_object_or_404(Cita, pk=id_cita)
            form = CitaForm(request.POST, instance=cita)
            form.save()
            return render(
                request,
                "detail_cita.html",
                {"Mensaje": "Cita actualizada exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_cita.html",
                {
                    "cita": cita,
                    "form": form,
                    "Mensaje": "ERROR actualizando la cita",
                },
            )

def delete_cita(request, id_cita):
    cita = get_object_or_404(Cita, pk=id_cita)
    if request.method == 'POST':
            cita.delete()
            return render(
                request,
                "detail_cita.html",
                {"Mensaje": "Cita eliminada exitosamente"})

# Factura/Boleta
# Lista todo (Factura/Boleta)
def fabo(request):
    fabos = FaBo.objects.all()
    return render(request, "fabo.html", {"fabos": fabos})


# Crea (Factura/Boleta)
def create_fabo(request):
    if request.method == "GET":
        return render(request, "create_fabo.html", {"form": FaBoForm})
    else:
        try:
            form = FaBoForm(request.POST)
            new_fabo = form.save()
            return render(
                request,
                "create_fabo.html",
                {"Mensaje": "Factura/Boleta guardada exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_fabo.html",
                {"form": FaBoForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Factura/Boleta)
def update_fabo(request, num_fb):
    if request.method == "GET":
        fabo = get_object_or_404(FaBo, pk=num_fb)
        form = FaBoForm(instance=fabo)
        return render(
            request, "detail_fabo.html", {"fabo": fabo, "form": form}
        )
    else:
        try:
            fabo = get_object_or_404(FaBo, pk=num_fb)
            form = FaBoForm(request.POST, instance=fabo)
            form.save()
            return render(
                request,
                "detail_fabo.html",
                {"Mensaje": "Factura/Boleta actualizada exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_fabo.html",
                {
                    "fabo": fabo,
                    "form": form,
                    "Mensaje": "ERROR actualizando la Factura/Boleta",
                },
            )

def delete_fabo(request, num_fb):
    fabo = get_object_or_404(FaBo, pk=num_fb)
    if request.method == 'POST':
            fabo.delete()
            return render(
                request,
                "detail_fabo.html",
                {"Mensaje": "Factura/Boleta eliminada exitosamente"})

# Vehículo
# Lista todo (Vehiculo)
def vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, "vehiculos.html", {"vehiculos": vehiculos})


# Crea (Vehiculo)
def create_vehiculo(request):
    if request.method == "GET":
        return render(request, "create_vehiculo.html", {"form": VehiculoForm})
    else:
        try:
            form = VehiculoForm(request.POST)
            new_vehiculo = form.save()
            return render(
                request,
                "create_vehiculo.html",
                {"Mensaje": "Vehiculo guardado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_vehiculo.html",
                {"form": VehiculoForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Vehiculo)
def update_vehiculo(request, patente):
    if request.method == "GET":
        vehiculo = get_object_or_404(Vehiculo, pk=patente)
        form = VehiculoForm(instance=vehiculo)
        return render(
            request, "detail_vehiculo.html", {"vehiculo": vehiculo, "form": form}
        )
    else:
        try:
            vehiculo = get_object_or_404(Vehiculo, pk=patente)
            form = VehiculoForm(request.POST, instance=vehiculo)
            form.save()
            return render(
                request,
                "detail_vehiculo.html",
                {"Mensaje": "Vehiculo actualizado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_vehiculo.html",
                {
                    "vehiculo": vehiculo,
                    "form": form,
                    "Mensaje": "ERROR actualizando el vehiculo",
                },
            )

def delete_vehiculo(request, patente):
    vehiculo = get_object_or_404(Vehiculo, pk=patente)
    if request.method == 'POST':
            vehiculo.delete()
            return render(
                request,
                "detail_vehiculo.html",
                {"Mensaje": "Vehiculo eliminado exitosamente"})

# Proveedor
# Lista todo (Proveedor)
def proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedores.html", {"proveedores": proveedores})


# Crea (Proveedor)
def create_proveedor(request):
    if request.method == "GET":
        return render(request, "create_proveedor.html", {"form": ProveedorForm})
    else:
        try:
            form = ProveedorForm(request.POST)
            new_proveedor = form.save()
            return render(
                request,
                "create_proveedor.html",
                {"Mensaje": "Proveedor guardado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_proveedor.html",
                {"form": ProveedorForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Proveedor)
def update_proveedor(request, id_prov):
    if request.method == "GET":
        proveedor = get_object_or_404(Proveedor, pk=id_prov)
        form = ProveedorForm(instance=proveedor)
        return render(
            request, "detail_proveedor.html", {"proveedor": proveedor, "form": form}
        )
    else:
        try:
            proveedor = get_object_or_404(Proveedor, pk=id_prov)
            form = ProveedorForm(request.POST, instance=proveedor)
            form.save()
            return render(
                request,
                "detail_proveedor.html",
                {"Mensaje": "Proveedor actualizado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_proveedor.html",
                {
                    "proveedor": proveedor,
                    "form": form,
                    "Mensaje": "ERROR actualizando el proveedor",
                },
            )

def delete_proveedor(request, id_prov):
    proveedor = get_object_or_404(Proveedor, pk=id_prov)
    if request.method == 'POST':
            proveedor.delete()
            return render(
                request,
                "detail_proveedor.html",
                {"Mensaje": "Proveedor eliminado exitosamente"})

# Pedido
# Lista todo (Pedido)
def pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, "pedidos.html", {"pedidos": pedidos})


# Crea (Pedido)
def create_pedido(request):
    if request.method == "GET":
        return render(request, "create_pedido.html", {"form": PedidoForm})
    else:
        try:
            form = PedidoForm(request.POST)
            new_pedido = form.save()
            return render(
                request,
                "create_pedido.html",
                {"Mensaje": "Pedido guardado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_pedido.html",
                {"form": PedidoForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Pedido)
def update_pedido(request, num_orden):
    if request.method == "GET":
        pedido = get_object_or_404(Pedido, pk=num_orden)
        form = PedidoForm(instance=pedido)
        return render(
            request, "detail_pedido.html", {"pedido": pedido, "form": form}
        )
    else:
        try:
            pedido = get_object_or_404(Pedido, pk=num_orden)
            form = PedidoForm(request.POST, instance=pedido)
            form.save()
            return render(
                request,
                "detail_pedido.html",
                {"Mensaje": "Pedido actualizado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_pedido.html",
                {
                    "pedido": pedido,
                    "form": form,
                    "Mensaje": "ERROR actualizando el pedido",
                },
            )

def delete_pedido(request, num_orden):
    pedido = get_object_or_404(Pedido, pk=num_orden)
    if request.method == 'POST':
            pedido.delete()
            return render(
                request,
                "detail_pedido.html",
                {"Mensaje": "Pedido eliminado exitosamente"})

# Producto
# Lista todo (Producto)
def productos(request):
    productos = Producto.objects.all()
    return render(request, "productos.html", {"productos": productos})


# Crea (Producto)
def create_producto(request):
    if request.method == "GET":
        return render(request, "create_producto.html", {"form": ProductoForm})
    else:
        try:
            form = ProductoForm(request.POST)
            new_producto = form.save()
            return render(
                request,
                "create_producto.html",
                {"Mensaje": "Producto guardado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "create_producto.html",
                {"form": ProductoForm, "Mensaje": "Por favor ingrese datos válidos"},
            )

# detail y Update (Producto)
def update_producto(request, id_prod):
    if request.method == "GET":
        producto = get_object_or_404(Producto, pk=id_prod)
        form = ProductoForm(instance=producto)
        return render(
            request, "detail_producto.html", {"producto": producto, "form": form}
        )
    else:
        try:
            producto = get_object_or_404(Producto, pk=id_prod)
            form = ProductoForm(request.POST, instance=producto)
            form.save()
            return render(
                request,
                "detail_producto.html",
                {"Mensaje": "Producto actualizado exitosamente"},
            )
        except ValueError:
            return render(
                request,
                "detail_producto.html",
                {
                    "producto": producto,
                    "form": form,
                    "Mensaje": "ERROR actualizando el producto",
                },
            )

def delete_producto(request, id_prod):
    producto = get_object_or_404(Producto, pk=id_prod)
    if request.method == 'POST':
            producto.delete()
            return render(
                request,
                "detail_producto.html",
                {"Mensaje": "Producto eliminado exitosamente"})
