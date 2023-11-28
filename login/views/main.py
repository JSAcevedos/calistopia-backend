from django.shortcuts import render
from ..models import Exercise


def main(request):
    catalogue = Exercise.objects.all()
    return render(request, "main.html", {
        'catalogue' : catalogue,
    })
