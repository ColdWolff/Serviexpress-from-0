from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def home(request):
    return render(request, "home.html")


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
                print("Usuario creado exitosamente")
                return HttpResponse("Usuario creado exitosamente")
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
