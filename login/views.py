from django.shortcuts import render, redirect
from .models import User
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

def signup(request):
    if request.POST['password'] == request.POST['confirm-password']:
        user = User(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
        user.password = make_password(user.password, salt=None, hasher='default')
        user = User.objects.filter(request.POST['username'])
        return render(request, 'index.html')
    else:
        print('User does not exist')
        return render(request, 'index.html')


def main(request):
    try:
        userName = request.POST["username"]
        if not User.objects.filter(username=userName).exists():
            userName = User.objects.get(email = userName).username
    except MultiValueDictKeyError:
        userName = False
    context = {"username": userName}
    return render(request, 'main.html')
