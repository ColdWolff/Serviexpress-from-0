from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def home(request):
    return render(request, "home.html")

def hnf(request):
    return render(request, "hnf.html")

def signup(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            # Registro de usuario
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                login(request,user)
                return redirect('index')
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "Error": "El usuario ya existe"},
                )
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "Error": "Las contraseñas no son iguales"},
        )

def index(request):
    return render(request, "index.html")