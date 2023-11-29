from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as cookie, logout as remove_cookie
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from ..models import History
from ..models import User
import datetime


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("main")

    remove_cookie(request)

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
                        cookie(request, user)
                        History.objects.create_history(request.user,"Login Exitoso")
                        return redirect("main")

                    else:
                        messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                        return redirect("login")
                else:
                    user = User.objects.get(username=userName)
                    user.todayLoginAttempts = userTodayLoginAttempts + 1
                    user.save()
                    userTodayLoginAttempts = User.objects.get(username=userName).todayLoginAttempts
                    messages.info(request, f"La contraseña ingresada no es correcta para {userName}.")
                    messages.info(request, f"Qeuedan {10 - userTodayLoginAttempts} intentos.")
                    History.objects.create_history(user,"Login Fallido")
                    return redirect("login")
            else:
                    History.objects.create_history(request.user,"Login Fallido")
                    messages.error(request, f"Lo sentimos. No tienes más intentos disponibles hoy.")
                    return redirect("login")
        elif User.objects.filter(email = userName.lower()).exists():
            userTodayLoginAttempts = User.objects.get(email=userName.lower()).todayLoginAttempts

            if now >= User.objects.get(email=userName.lower()).lastLoginAttemptDate + datetime.timedelta(1):
                user = User.objects.get(email=userName.lower())
                user.todayLoginAttempts = 0
                user.save()

            if userTodayLoginAttempts != 10:
                password = User.objects.get(email=userName.lower()).password
                if check_password(userPassword, password):
                    if User.objects.get(email = userName.lower()).active:
                        user = User.objects.get(email=userName.lower())
                        user.todayLoginAttempts = 0
                        user.save()
                        cookie(request, user)
                        return redirect("main")
                    else:
                        messages.info(request, f"La cuenta no ha sido activa, porfavor usa el link enviado a tu correo para activarla.")
                        return redirect("login")
                else:
                    user = User.objects.get(email=userName.lower())
                    user.todayLoginAttempts = userTodayLoginAttempts + 1
                    user.save()
                    userTodayLoginAttempts = User.objects.get(email=userName.lower()).todayLoginAttempts
                    messages.info(request, f"La contraseña ingresada no es correcta para {userName.lower()}.")
                    messages.info(request, f"Quedan {10 - userTodayLoginAttempts} intentos.")
                    History.objects.create_history(request.user,"Login Fallido")
                    return redirect("login")
            else:
                History.objects.create_history(request.user,"Login Fallido")
                messages.error(request, f"Lo sentimos. No tienes más intentos disponibles hoy.")
                return redirect("login")
        else:
            messages.error(request, "El nombre de usuario o correo electrónico no se encuentra registrado.")
            return redirect("login")
    except MultiValueDictKeyError:
        userName = False
        userPassword = False
    return render(request, 'login_register/login.html')

def logout(request):
    History.objects.create_history(request.user,"Logout Exitoso")
    remove_cookie(request)
    return redirect("login")

