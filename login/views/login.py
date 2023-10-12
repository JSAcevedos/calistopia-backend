from django.shortcuts import render, redirect
from ..models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

# Create your views here.

def login(request):
    try:
        userName = request.POST['username']
        userPassword = request.POST['password']

        if User.objects.filter(username = userName).exists():
            password = User.objects.get(username = userName).password
            if check_password(userPassword, password):
                if User.objects.get(username = userName).active:
                    return redirect("main")
                else:
                    messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                    return redirect("index")
            else:
                messages.error(request, f"La contraseña ingresada no es correcta para {userName}.")
                return redirect("index")
        elif User.objects.filter(email = userName).exists():
            password = User.objects.get(email=userName).password
            if check_password(userPassword, password):
                if User.objects.get(email = userName).active:
                    return redirect("main")
                else:
                    messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                    return redirect("index")
            else:
                messages.error(request, f"La contraseña ingresada no es correcta para {userName}.")
                return redirect("index")
        else:
            messages.error(request, "El nombre de usuario o correo electrónico no se encuentra registrado.")
            return redirect("index")
    except MultiValueDictKeyError:
        userName = False
        userPassword = False
    return render(request, 'index.html')

def logout(request):
    return redirect("index")

