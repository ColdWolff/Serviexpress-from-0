import re
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.password_validation import validate_password

from .forms import (
    CitaForm,
    ServicioForm,
    FaBoForm,
    VehiculoForm,
    ProveedorForm,
    PedidoForm,
    ProductoForm,
    ClienteForm,
    EmpleadoForm,
)
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

def formatear_rut(rut):
    rut = rut.replace('.', '').replace('-', '').replace(' ', '')
    
    if len(rut) > 9:
        rut = '{}-{}'.format(rut[:-1], rut[-1])
    
    rut_formateado = '{}.{}.{}-{}'.format(rut[:2], rut[2:5], rut[5:8], rut[8:])
    
    return rut_formateado

def hnf(request):
        return render(request, "hnf.html")

#Vizualizaciones
def home(request):
    if request.user.is_authenticated:
        rol = ""
        try:
            cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
            rol = "Cliente"
        except Cliente.DoesNotExist:
            pass
        try:
            empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
            rol = "Empleado"
        except Empleado.DoesNotExist:
            pass
        return render(
            request,
            "home.html",
            {
                "rol": rol,
                "cliente": cliente,
                "empleado": empleado
            },
        )
    else:
        return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        if len(password1) <8:
            return render(
            request,
            "signup.html",
            {"Mensaje": "Error en la contraseña: Tiene menos de 8 caracteres"},
        )

        if password1 != password2:
            return render(
                request, "signup.html", {"Mensaje": "Las contraseñas no coinciden"}
            )
        else:
            rol = request.POST["role"]
            rut = request.POST["rut"]
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            
            rut= formatear_rut(rut)
            usuario_existente = Cliente.objects.filter(rut_cli=rut).exists()
            usuario_existente2 = Empleado.objects.filter(rut_emp=rut).exists()
            if usuario_existente or usuario_existente2:
                return render(
                    request,
                    "signup.html",
                    {"Mensaje": "El usuario ya existe en la base de datos."},
                )

            # Crear el usuario si no existe
            try:
                if rol == "Cliente":
                    cliente = Cliente.objects.create(
                        rut_cli=rut,
                        pnom_cli=nombre,
                        appaterno_cli=apellido,
                    )
                    user = User.objects.create_user(username=rut, password=password1)
                elif rol == "Empleado":
                    empleado = Empleado.objects.create(
                        rut_emp=rut,
                        pnom_emp=nombre,
                        appaterno_emp=apellido,
                    )
                    user = User.objects.create_user(username=rut, password=password1)
                login(request, user)
                return redirect("home")
            except Exception:
                return render(
                    request, "signup.html", {"Mensaje": "Error al crear usuario"}
                )

    return render(request, "signup.html", {"Mensaje": "Método HTTP no permitido"})

def signin(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signin.html")
    else:
        rut= formatear_rut(request.POST["username"])
        user = authenticate(
            request,
            username=rut,
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

# Detail y Update (Cliente)
@login_required
def update_user(request, username):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    Mensaje = ""

    if cliente:
        form = ClienteForm(instance=cliente)
        if request.method == "POST":
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                Mensaje = "Datos actualizados correctamente"
        return render(
            request,
            "perfil_cli.html",
            {"cliente": cliente, "form": form, "Mensaje": Mensaje},
        )

    elif empleado:
        form = EmpleadoForm(instance=empleado)
        if request.method == "POST":
            form = EmpleadoForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                Mensaje = "Datos actualizados correctamente"

        return render(
            request,
            "perfil_emp.html",
            {"empleado": empleado, "form": form, "Mensaje": Mensaje},
        )

    else:
        return HttpResponse("Perfil no encontrado para este usuario")

def signout(request):
    logout(request)
    return redirect("home")

# Lista todo (Servicio)
def servicios(request):
    servicios = Servicio.objects.all()
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    
    return render(
        request,
        "servicios.html",
        {"servicios": servicios, "cliente": cliente, "empleado": empleado, "rol": rol},
    )


# Crea (Servicio)
@login_required
def create_servicio(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_servicio.html",
            {"form": ServicioForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            form = ServicioForm(request.POST)
            new_servicio = form.save()
            return render(
                request,
                "create_servicio.html",
                {
                    "Mensaje": "Servicio guardado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "create_servicio.html",
                {
                    "form": ServicioForm,
                    "Mensaje": "Por favor ingrese datos válidos",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Servicio)
@login_required
def update_servicio(request, id_serv):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        servicio = get_object_or_404(Servicio, pk=id_serv)
        form = ServicioForm(instance=servicio)
        return render(
            request,
            "detail_servicio.html",
            {
                "servicio": servicio,
                "form": form,
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )
    else:
        try:
            servicio = get_object_or_404(Servicio, pk=id_serv)
            form = ServicioForm(request.POST, instance=servicio)
            form.save()
            return render(
                request,
                "detail_servicio.html",
                {
                    "Mensaje": "Servicio actualizado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_servicio.html",
                {
                    "servicio": servicio,
                    "form": form,
                    "Mensaje": "ERROR actualizando el servicio",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_servicio(request, id_serv):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    servicio = get_object_or_404(Servicio, pk=id_serv)
    if request.method == "POST":
        servicio.delete()
        return render(
            request,
            "detail_servicio.html",
            {
                "Mensaje": "Servicio eliminado exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )


# Citas
# Lista todo (Cita)
@login_required
def citas(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if empleado:
        citas = Cita.objects.all()
    elif cliente:
        citas = Cita.objects.filter(cliente=cliente)
    return render(
        request,
        "citas.html",
        {"citas": citas, "cliente": cliente, "empleado": empleado},
    )


# Crea (Cita)
@login_required
def create_cita(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_cita.html",
            {"form": CitaForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        form = CitaForm(request.POST)
        if form.is_valid():
            try:
                new_cita = form.save(commit=False)
                new_cita.cliente = cliente
                new_cita.save()

                servicios_seleccionados = request.POST.getlist('servicios')
                for servicio_id in servicios_seleccionados:
                    servicio = Servicio.objects.get(pk=servicio_id)
                    new_cita.servicios.add(servicio)

                return render(
                    request,
                    "create_cita.html",
                    {
                        "Mensaje": "Cita guardada exitosamente",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )
            except ValueError:
                return render(
                    request,
                    "create_cita.html",
                    {
                        "form": CitaForm,
                        "Mensaje": "Por favor ingrese datos válidos",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )
        else:
            return render (
                request,
                "create_cita.html",
                {
                    "form": CitaForm,
                    "Mensaje": "Seleccione un día hábil o una hora que no haya sido agendada",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Cita)
@login_required
def update_cita(request, id_cita):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"

    cita = get_object_or_404(Cita, pk=id_cita)
    if request.method == "GET":
        form = CitaForm(instance=cita)
        return render(
            request,
            "detail_cita.html",
            {"cita": cita, "form": form, "cliente": cliente, "empleado": empleado},
        )
    else:
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            try:
                
                updated_cita = form.save(commit=False)
                updated_cita.save()
                
                servicios_seleccionados = request.POST.getlist('servicios')
                cita.servicios.clear()  # Eliminar los servicios asociados actualmente
                for servicio_id in servicios_seleccionados:
                    servicio = Servicio.objects.get(pk=servicio_id)
                    cita.servicios.add(servicio)

                return render(
                    request,
                    "detail_cita.html",
                    {
                        "Mensaje": "Cita actualizada exitosamente",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )
            except ValueError:
                return render(
                    request,
                    "detail_cita.html",
                    {
                        "cita": cita,
                        "form": form,
                        "Mensaje": "ERROR actualizando la cita",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )

@login_required
def delete_cita(request, id_cita):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    cita = get_object_or_404(Cita, pk=id_cita)
    if request.method == "POST":
        cita.delete()
        return render(
            request,
            "detail_cita.html",
            {
                "Mensaje": "Cita eliminada exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )


# Factura/Boleta
# Lista todo (Factura/Boleta)
@login_required
def fabo(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    fabos = FaBo.objects.none() 

    if cliente:
        citas_cliente = Cita.objects.filter(cliente=cliente)
        fabos = FaBo.objects.filter(cita__in=citas_cliente)
    else:
        fabos = FaBo.objects.all()

    return render(
        request, "fabo.html", {"fabos": fabos, "cliente": cliente, "empleado": empleado}
    )

@login_required
def create_fabo(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"

    if request.method == "GET":
        cita_id = request.GET.get('cita_id')
        cita = Cita.objects.get(pk=cita_id) if cita_id else None
        servicios = cita.servicios.all() if cita else None

        return render(
            request,
            "create_fabo.html",
            {"form": FaBoForm(servicios=servicios), "cliente": cliente, "empleado": empleado},
        )
    else:
        form = FaBoForm(request.POST)
        if form.is_valid():
            try:
                new_fabo = form.save(commit=False)
                cita = new_fabo.cita
                total_pagar = cita.servicios.aggregate(total=Sum('costo_serv'))['total']
                new_fabo.totalpagar = total_pagar
                new_fabo.save()

                # Guardar la relación muchos a muchos después de que num_fb tenga un valor
                new_fabo.detalle_fb.set(cita.servicios.all())

                return render(
                    request,
                    "create_fabo.html",
                    {
                        "Mensaje": "Factura/Boleta guardada exitosamente",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )
            except ValueError as e:
                print(f"Error al guardar Factura/Boleta: {e}")
                return render(
                    request,
                    "create_fabo.html",
                    {
                        "form": FaBoForm(),
                        "Mensaje": "Por favor ingrese datos válidos",
                        "cliente": cliente,
                        "empleado": empleado,
                        "rol": rol,
                    },
                )

# detail y Update (Factura/Boleta)
@login_required
def update_fabo(request, num_fb):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        fabo = get_object_or_404(FaBo, pk=num_fb)
        form = FaBoForm(instance=fabo)
        return render(
            request,
            "detail_fabo.html",
            {"fabo": fabo, "form": form, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            fabo = get_object_or_404(FaBo, pk=num_fb)
            form = FaBoForm(request.POST, instance=fabo)
            form.save()
            return render(
                request,
                "detail_fabo.html",
                {
                    "Mensaje": "Factura/Boleta actualizada exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_fabo.html",
                {
                    "fabo": fabo,
                    "form": form,
                    "Mensaje": "ERROR actualizando la Factura/Boleta",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_fabo(request, num_fb):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    fabo = get_object_or_404(FaBo, pk=num_fb)
    if request.method == "POST":
        fabo.delete()
        return render(
            request,
            "detail_fabo.html",
            {
                "Mensaje": "Factura/Boleta eliminada exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )

# Vehículo
# Lista todo (Vehiculo)
@login_required
def vehiculos(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    if empleado:
        vehiculos = Vehiculo.objects.all()
    elif cliente:
        vehiculos = Vehiculo.objects.filter(cliente=cliente)
    return render(
        request,
        "vehiculos.html",
        {"vehiculos": vehiculos, "cliente": cliente, "empleado": empleado},
    )


# Crea (Vehiculo)
@login_required
def create_vehiculo(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_vehiculo.html",
            {"form": VehiculoForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            form = VehiculoForm(request.POST)
            new_vehiculo = form.save(commit=False)
            new_vehiculo.cliente = cliente
            new_vehiculo.save()
            return render(
                request,
                "create_vehiculo.html",
                {
                    "Mensaje": "Vehiculo guardado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "create_vehiculo.html",
                {
                    "form": VehiculoForm,
                    "Mensaje": "Por favor ingrese datos válidos",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Vehiculo)
@login_required
def update_vehiculo(request, patente):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        vehiculo = get_object_or_404(Vehiculo, pk=patente)
        form = VehiculoForm(instance=vehiculo)
        return render(
            request,
            "detail_vehiculo.html",
            {
                "vehiculo": vehiculo,
                "form": form,
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )
    else:
        try:
            vehiculo = get_object_or_404(Vehiculo, pk=patente)
            form = VehiculoForm(request.POST, instance=vehiculo)
            form.save()
            return render(
                request,
                "detail_vehiculo.html",
                {
                    "Mensaje": "Vehiculo actualizado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_vehiculo.html",
                {
                    "vehiculo": vehiculo,
                    "form": form,
                    "Mensaje": "ERROR actualizando el vehiculo",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_vehiculo(request, patente):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    vehiculo = get_object_or_404(Vehiculo, pk=patente)
    if request.method == "POST":
        vehiculo.delete()
        return render(
            request,
            "detail_vehiculo.html",
            {
                "Mensaje": "Vehiculo eliminado exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )


# Proveedor
# Lista todo (Proveedor)
@login_required
def proveedores(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    proveedores = Proveedor.objects.all()
    return render(
        request,
        "proveedores.html",
        {"proveedores": proveedores, "cliente": cliente, "empleado": empleado},
    )


# Crea (Proveedor)
@login_required
def create_proveedor(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_proveedor.html",
            {"form": ProveedorForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            form = ProveedorForm(request.POST)
            new_proveedor = form.save()
            return render(
                request,
                "create_proveedor.html",
                {
                    "Mensaje": "Proveedor guardado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "create_proveedor.html",
                {
                    "form": ProveedorForm,
                    "Mensaje": "Por favor ingrese datos válidos",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Proveedor)
@login_required
def update_proveedor(request, id_prov):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        proveedor = get_object_or_404(Proveedor, pk=id_prov)
        form = ProveedorForm(instance=proveedor)
        return render(
            request,
            "detail_proveedor.html",
            {
                "proveedor": proveedor,
                "form": form,
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )
    else:
        try:
            proveedor = get_object_or_404(Proveedor, pk=id_prov)
            form = ProveedorForm(request.POST, instance=proveedor)
            form.save()
            return render(
                request,
                "detail_proveedor.html",
                {
                    "Mensaje": "Proveedor actualizado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_proveedor.html",
                {
                    "proveedor": proveedor,
                    "form": form,
                    "Mensaje": "ERROR actualizando el proveedor",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_proveedor(request, id_prov):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    proveedor = get_object_or_404(Proveedor, pk=id_prov)
    if request.method == "POST":
        proveedor.delete()
        return render(
            request,
            "detail_proveedor.html",
            {
                "Mensaje": "Proveedor eliminado exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )

# Pedido
# Lista todo (Pedido)
@login_required
def pedidos(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    pedidos = Pedido.objects.all()
    return render(
        request,
        "pedidos.html",
        {"pedidos": pedidos, "cliente": cliente, "empleado": empleado},
    )


# Crea (Pedido)
@login_required
def create_pedido(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_pedido.html",
            {"form": PedidoForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            form = PedidoForm(request.POST)
            new_pedido = form.save()
            return render(
                request,
                "create_pedido.html",
                {
                    "Mensaje": "Pedido guardado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "create_pedido.html",
                {
                    "form": PedidoForm,
                    "Mensaje": "Por favor ingrese datos válidos",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Pedido)
@login_required
def update_pedido(request, num_orden):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        pedido = get_object_or_404(Pedido, pk=num_orden)
        form = PedidoForm(instance=pedido)
        return render(
            request,
            "detail_pedido.html",
            {"pedido": pedido, "form": form, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            pedido = get_object_or_404(Pedido, pk=num_orden)
            form = PedidoForm(request.POST, instance=pedido)
            form.save()
            return render(
                request,
                "detail_pedido.html",
                {
                    "Mensaje": "Pedido actualizado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_pedido.html",
                {
                    "pedido": pedido,
                    "form": form,
                    "Mensaje": "ERROR actualizando el pedido",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_pedido(request, num_orden):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    pedido = get_object_or_404(Pedido, pk=num_orden)
    if request.method == "POST":
        pedido.delete()
        return render(
            request,
            "detail_pedido.html",
            {
                "Mensaje": "Pedido eliminado exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )


# Producto
# Lista todo (Producto)
@login_required
def productos(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    productos = Producto.objects.all()
    return render(
        request,
        "productos.html",
        {"productos": productos, "cliente": cliente, "empleado": empleado},
    )


# Crea (Producto)
@login_required
def create_producto(request):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        return render(
            request,
            "create_producto.html",
            {"form": ProductoForm, "cliente": cliente, "empleado": empleado},
        )
    else:
        try:
            form = ProductoForm(request.POST)
            new_producto = form.save()
            return render(
                request,
                "create_producto.html",
                {
                    "Mensaje": "Producto guardado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "create_producto.html",
                {
                    "form": ProductoForm,
                    "Mensaje": "Por favor ingrese datos válidos",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )


# detail y Update (Producto)
@login_required
def update_producto(request, id_prod):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    if request.method == "GET":
        producto = get_object_or_404(Producto, pk=id_prod)
        form = ProductoForm(instance=producto)
        return render(
            request,
            "detail_producto.html",
            {
                "producto": producto,
                "form": form,
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )
    else:
        try:
            producto = get_object_or_404(Producto, pk=id_prod)
            form = ProductoForm(request.POST, instance=producto)
            form.save()
            return render(
                request,
                "detail_producto.html",
                {
                    "Mensaje": "Producto actualizado exitosamente",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )
        except ValueError:
            return render(
                request,
                "detail_producto.html",
                {
                    "producto": producto,
                    "form": form,
                    "Mensaje": "ERROR actualizando el producto",
                    "cliente": cliente,
                    "empleado": empleado,
                    "rol": rol,
                },
            )

@login_required
def delete_producto(request, id_prod):
    cliente = Cliente.objects.filter(rut_cli=request.user.username).first()
    empleado = Empleado.objects.filter(rut_emp=request.user.username).first()
    rol = "Cliente" if cliente else "Empleado"
    producto = get_object_or_404(Producto, pk=id_prod)
    if request.method == "POST":
        producto.delete()
        return render(
            request,
            "detail_producto.html",
            {
                "Mensaje": "Producto eliminado exitosamente",
                "cliente": cliente,
                "empleado": empleado,
                "rol": rol,
            },
        )
