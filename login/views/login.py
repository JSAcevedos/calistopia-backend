from django.shortcuts import render, redirect
from ..models import User
from django.contrib.auth.hashers import make_password
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import auth
from django.contrib import messages

# Create your views here.

def login(request):
    try:
        userName = request.POST['username']
        userPassword = make_password(request.POST['password'], salt=None, hasher='default')
        

        if User.objects.filter(username = userName).exists():
            password = User.objects.get(username = userName).password
            if password == userPassword:
                return redirect("main")
            else:
                messages.info(request, "La contraseña ingresada no es correcta.")
                return redirect("login")
        elif User.objects.filter(email = userName).exists():
            password = User.objects.get(email=userName).password
            if password == userPassword:
                return redirect("main")
            else:
                messages.info(request, "La contraseña ingresada no es correcta.")
                return redirect("login")
        else:
            messages.info(request, "El nombre de usuario o correo electrónico no se encuentra registrado.")
            return redirect("login")
    except MultiValueDictKeyError:
        userName = False
        userPassword = False
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

