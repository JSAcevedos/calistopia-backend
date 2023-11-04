from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as cookie, logout as remove_cookie
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from ..models import User
from .login import logout
import datetime

def config(request):
    return render(request, "config.html")

def change_config(request, id):
    try:
        if id == "password":
            context = {"id": "Nueva contraseña", "pass": True}
            password = request.POST["data"]
            confirm_password = request.POST["confirm_password"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username = request.user.username)
            user_password = user.password

            if check_password(current_password, user_password):
                if password == confirm_password:
                    user.password = password
                    user.save()
                    messages.info(request, f"La contraseña ha sido cambiada.")
                    return redirect("logout")
                else:
                    messages.info(request, f"Las nuevas contraseñas no coinciden.")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")
        elif id == "username":
            context = {"id": "Nuevo nombre de Usuario", "pass": False}
            new_username = request.POST["data"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if  check_password(current_password, user_password):
                user.username = new_username
                user.save()
                messages.info(request, f"El nombre de usuario ha sido modificado.")
                return redirect("logout")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")
        elif id == "email":
            context =  {"id": "Nuevo correo electrónico", "pass": False}
            new_email = request.POST["data"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if check_password(current_password, user_password):
                messages.info(request, f"No implementado aún.")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")

        elif id == "login":
            return redirect("login")
        else:
            return redirect("logout")
    except MultiValueDictKeyError:
        pass
    return render(request, "changes.html", context = context)