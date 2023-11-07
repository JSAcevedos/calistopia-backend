from django.shortcuts import render
from ..models import Exercise

def exercise(request, exercise_id):
    exercise = Exercise.objects.get(id = exercise_id)
    related = Exercise.objects.filter(level = exercise.level, group = exercise.group).exclude(id = exercise.id)
    return render(request, "exercise.html", {
        'exercise' : exercise,
        'related' : related
    })

