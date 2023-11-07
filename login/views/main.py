from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request,"pagina_principal.html")