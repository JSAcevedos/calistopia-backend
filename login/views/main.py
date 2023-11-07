from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def main(request):
    if request.user.is_authenticated:
        return render(request, "principalIngresado.html")
    else:
        return render(request,"paginaPrincipal.html")