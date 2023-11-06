from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from ..tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib import messages
from ..models import User

@login_required
def config(request):
    return render(request, "config.html")

@login_required
def change_config(request, id):
    try:
        if id == "password":
            context = {"id": "Nueva contraseña", "pass": True}
            password = request.POST["data"]
            confirm_password = request.POST["confirm_password"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username = request.user.username)
            user_password = user.password

            if check_password(current_password, user_password):
                if password == confirm_password:
                    user.password = password
                    user.save()
                    messages.info(request, f"La contraseña ha sido cambiada.")
                    return redirect("logout")
                else:
                    messages.info(request, f"Las nuevas contraseñas no coinciden.")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")
        elif id == "username":
            context = {"id": "Nuevo nombre de Usuario", "pass": False}
            new_username = request.POST["data"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if  check_password(current_password, user_password):
                user.username = new_username
                user.save()
                messages.info(request, f"El nombre de usuario ha sido modificado.")
                return redirect("logout")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")
        elif id == "email":
            context =  {"id": "Nuevo correo electrónico", "pass": False}
            new_email = request.POST["data"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if check_password(current_password, user_password):
                confirm_email(request, user, new_email)
                return redirect("main")
            else:
                messages.info(request, f"La contraseña actual no es correcta.")
        else:
            return redirect("logout")
    except MultiValueDictKeyError:
        pass
    return render(request, "changes.html", context = context)

def confirm_email(request, user, to_email):
        mail_subject = "Confirma tu correo en calistopia"
        message = render_to_string(
            "confirm_email.html",
            {
                "user": user.username,
                "domain": request.get_host,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "email": to_email,
                "protocol": "https" if request.is_secure() else "http",
            },
        )
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

def email_confirmated(request, uidb64, token, email):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email = email
        user.save()
        messages.info(request, f"El correo ha sido cambiado exitosamente.")
        return redirect("logout")
    else:
        return HttpResponse(
            "¡Link invalido!"
        )