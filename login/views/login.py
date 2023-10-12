from django.shortcuts import render, redirect
from ..models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.utils import timezone
import datetime


# Create your views here.

def login(request):
    try:
        userName = request.POST['username']
        userPassword = request.POST['password']
        now = timezone.now()
        if User.objects.filter(username = userName).exists():
            userTodayLoginAttempts = User.objects.get(username=userName).todayLoginAttempts

            if now >= User.objects.get(username = userName).lastLoginAttemptDate + datetime.timedelta(1):
                user = User.objects.get(username=userName)
                user.todayLoginAttempts = 0
                user.save()

            if userTodayLoginAttempts != 10:
                password = User.objects.get(username = userName).password
                if check_password(userPassword, password):
                    if User.objects.get(username = userName).active:
                        user = User.objects.get(username=userName)
                        user.todayLoginAttempts = 0
                        user.save()
                        return redirect("main")
                    else:
                        messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                        return redirect("index")
                else:
                    user = User.objects.get(username=userName)
                    user.todayLoginAttempts = userTodayLoginAttempts + 1
                    user.save()
                    userTodayLoginAttempts = User.objects.get(username=userName).todayLoginAttempts
                    messages.info(request, f"La contraseña ingresada no es correcta para {userName}.")
                    messages.info(request, f"Qeuedan {10 - userTodayLoginAttempts} intentos.")
                    return redirect("index")
            else:
                    messages.error(request, f"Lo sentimos. No tienes más intentos disponibles hoy.")
                    return redirect("index")
        elif User.objects.filter(email = userName).exists():
            userTodayLoginAttempts = User.objects.get(email=userName).todayLoginAttempts

            if now >= User.objects.get(email=userName).lastLoginAttemptDate + datetime.timedelta(1):
                user = User.objects.get(email=userName)
                user.todayLoginAttempts = 0
                user.save()

            if userTodayLoginAttempts != 10:
                password = User.objects.get(email=userName).password
                if check_password(userPassword, password):
                    if User.objects.get(email = userName).active:
                        user = User.objects.get(email=userName)
                        user.todayLoginAttempts = 0
                        user.save()
                        return redirect("main")
                    else:
                        messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                        return redirect("index")
                else:
                    user = User.objects.get(username=userName)
                    user.todayLoginAttempts = userTodayLoginAttempts + 1
                    user.save()
                    userTodayLoginAttempts = User.objects.get(email=userName).todayLoginAttempts
                    messages.info(request, f"La contraseña ingresada no es correcta para {userName}.")
                    messages.info(request, f"Qeuedan {10 - userTodayLoginAttempts} intentos.")
                    return redirect("index")
            else:
                messages.error(request, f"Lo sentimos. No tienes más intentos disponibles hoy.")
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

