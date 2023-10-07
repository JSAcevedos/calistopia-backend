from django.http import HttpResponseNotFound, HttpResponse
from django.contrib.auth.hashers import make_password
from ..models import User

def signup(request):

# Register User

    if request.method == 'GET':
        return HttpResponseNotFound("<h1>Not Found<h1>")
    else:
        try:
            if request.POST['password'] == request.POST['confirm-password']:
                user = User(username = request.POST['username'],password = request.POST['password'], email = request.POST['email'])
                user.password = make_password(user.password, salt=None, hasher='default')
                user.save()
                return HttpResponse('User created')
            else:
                return HttpResponse('Password does not match')
        except:
            return HttpResponse('The user already exist')