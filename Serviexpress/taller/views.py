from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CitaForm, ServicioForm
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
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signup.html")
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # Registro de usuario
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                login(request, user)
                return redirect("index")
            except:
                return render(request, "signup.html", {"Mensaje": "El usuario ya existe"})
        return render(
            request,
            "signup.html",
            {"Mensaje": "Las contraseñas no son iguales"},
        )

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
            return redirect("index")


def signout(request):
    logout(request)
    return redirect("home")


def index(request):
    return render(request, "index.html")

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
            return render(request, "create_servicio.html", {"Mensaje": "Servicio guardado exitosamente"})
        except ValueError:
            return render(
                request,
                "create_servicio.html",
                {"form": ServicioForm, "Mensaje": "Por favor ingrese datos válidos"},
            )


# Lista con parametro 
#def citas_filter(request):
    # cita = Citas.objects.filter(user = request.user)
    #return render(request, "citas.html", {"citas": citas})