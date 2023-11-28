from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from ..models import Exercise
from ..models import Routine
from ..models import History

@login_required
def routine(request, routine_id):

    routine = Routine.objects.get(id = routine_id)
    title = routine.name
    exercises = []
    description = {
        'item':0,
        'series':0,
        'cycles':0,
        'rest':0
    }
    feature = 0

    for i in routine.exercises:
        
        description['item'] = Exercise.objects.get(id = i)
        description['series'] = routine.description[feature+0]
        description['cycles'] = routine.description[feature+1]
        description['rest'] = routine.description[feature+2]
        exercises.append(description.copy())
        feature += 3

    return render(request, "routine/routine.html",{
        'exercises': exercises,
        'title' : title,
        'routine_id' : routine_id
    })

@login_required
def modify_routine(request, routine_id):
    catalogue = Exercise.objects.all()
    if request.method == "GET":
        
        routine = Routine.objects.get(id=routine_id).exercises
        description = Routine.objects.get(id=routine_id).description
        routine_name = Routine.objects.get(id=routine_id).name
        exercises = []
        index = 0
        data = {
            'name':'',
            'logo':'',
            'group':'',
            'series':'',
            'cycles':'',
            'rest':''
        }

        for i in routine:
            temp = Exercise.objects.get(id=i)

            data['name'] = temp.name
            data['logo'] = temp.logo
            data['group'] = temp.group

            data['series'] = description[index+0]
            data['cycles'] = description[index+1]
            data['rest'] = description[index+2]
            exercises.append(data.copy())
            index += 3

        return render(request, "routine/modify_routine.html", {
            'catalogue' : catalogue,
            'routine_id' : routine_id,
            'routine_name' : routine_name,
            'exercises' : exercises

        })
    else:
        exercises_names = request.POST['routine'].split(',')
        description = request.POST['description'].split(',')
        exercises = []

        for exercise in exercises_names:
            id = Exercise.objects.get(name=exercise).id
            exercises.append(id)

        new_routine = Routine.objects.get(id = routine_id)

        if request.POST['title']:
            title = request.POST['title']
            new_routine.name = title
        
        new_routine.exercises = exercises
        new_routine.description = description
        new_routine.save()
        History.objects.create_history(request.user,"Rutina modificada")
        return redirect(f"/routines/{routine_id}/")

@login_required
def create_routine(request):
    catalogue = Exercise.objects.all()
    if request.method == "GET":
        return render(request, "routine/create_routine.html", {
            'catalogue' : catalogue
        })
    else:
        title = request.POST['title']
        exercises_names = request.POST['routine'].split(',')
        description = request.POST['description'].split(',')
        exercises = []
        user_id = request.user

        for exercise in exercises_names:
            id = Exercise.objects.get(name=exercise).id
            exercises.append(id)
         
        logo = Exercise.objects.get(name = exercises_names[0]).logo

        Routine.objects.create_routine(user_id, exercises, title, description, logo)

        History.objects.create_history(request.user,"Rutina creada")

        return render(request, "routine/create_routine.html", {
            'catalogue' : catalogue
        })

@login_required
def delete_routine(request, routine_id):

    if request.method == "GET":
        return Http404
    else:
        
        routine = Routine.objects.get(id=routine_id)
        routine.delete()

        user = request.user
        History.objects.create_history(user,"Rutina eliminada")
        routines = Routine.objects.filter(user_id=user)
        history = History.objects.filter(user_id=user)

        return render(request, "vista_user.html", {
            'routines': routines,
            'username': user,
            'history' : history
        })
                
