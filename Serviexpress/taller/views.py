from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


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
                return render(
                    request,
                    "signup.html",
                    {"Error": "El usuario ya existe"}
                )
        return render(
            request,
            "signup.html",
            {"Error": "Las contraseñas no son iguales"},
        )


def signin(request):
    if request.method == "GET":
        print("Desplegando formulario")
        return render(request, "signin.html")
    else:
        try:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
            )
            login(request, user)
            return redirect("index")
        except:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "Error": "El usuario ya existe"},
            )


def index(request):
    return render(request, "index.html")


def signout(request):
    logout(request)
    return redirect("home")
