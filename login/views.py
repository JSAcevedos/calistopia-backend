from django.shortcuts import render
from .models import User
from django.contrib.auth.hashers import make_password

# Create your views here.

def login(request):
    return render(request, 'index.html')
    
def signup(request):
    if request.POST['password'] == request.POST['confirm-password']:
        user = User(username = request.POST['username'],password = request.POST['password'], email = request.POST['email'])
        user.password = make_password(user.password, salt=None, hasher='default')
        user = User.objects.filter(request.POST['username'])
        return render(request, 'index.html')
    else:
        print('User does not exist')
        return render(request, 'index.html')
