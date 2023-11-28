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
from ..models import History
from ..models import Routine
from ..models import User

@login_required
def user_view(request):
    user = request.user
    routines = Routine.objects.filter(user_id=user)
    history = History.objects.filter(user_id=request.user)

    return render(request, "vista_user.html", {
        'routines':routines,
        'username':request.user,
        'history' : history
    })

@login_required
def config(request):
    messages.info(request,"Para efectuar los cambios debes ingresar tu contraseña.")
    return render(request, "config/data_modify.html")

@login_required
def change_config(request, id):
    try:
        if id == "password":
            password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username = request.user.username)
            user_password = user.password

            if not len(password):
                messages.error(request, f"Contraseña no válida.")
                return redirect("/user/config/")

            if not len(confirm_password):
                messages.error(request, f"Por favor confirma tu nueva contraseña.")
                return redirect("/user/config/")

            if check_password(current_password, user_password):
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    messages.success(request, f"La contraseña ha sido cambiada.")
                    return redirect("logout")
                else:
                    messages.error(request, f"Las nuevas contraseñas no coinciden.")
                    return redirect("/user/config/")
            else:
                messages.error(request, f"La contraseña actual no es correcta.")
                return redirect("/user/config/")
        elif id == "username":
            new_username = request.POST["new_username"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if not len(new_username):
                messages.error(request, f"Nombre de usuario no válido.")
                return redirect("/user/config/")
            if  check_password(current_password, user_password):
                user.username = new_username
                user.save()
                messages.success(request, f"El nombre de usuario ha sido modificado.")
                return redirect("logout")
            else:
                messages.error(request, f"La contraseña actual no es correcta.")
                return redirect("/user/config/")
        elif id == "email":
            new_email = request.POST["new_email"]
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password
            if not len(new_email):
                messages.error(request, f"Correo electrónico no válido.")
                return redirect("/user/config/")
            if check_password(current_password, user_password):
                confirm_email(request, user, new_email)
                messages.info(request, f"Por favor, confirma tu correo para guardar el cambio.")
                return redirect("/user/config/")
            else:
                messages.error(request, f"La contraseña actual no es correcta.")
                return redirect("/user/config/")
        elif id == "delete":
            current_password = request.POST["curr_password"]

            user = User.objects.get(username=request.user.username)
            user_password = user.password

            if check_password(current_password, user_password):
                user.delete()
                messages.info(request, f"Usuario eliminado satisfactoriamente.")
                return redirect("logout")
            else:
                messages.error(request, f"La contraseña actual no es correcta.")
                return redirect("/user/config/")
        else:
            return redirect("logout")
    except MultiValueDictKeyError:
        messages.info(request, f"Lo sentimos, ha ocurrido un error, intentalo más tarde.")
        return redirect("/user/config/")

def confirm_email(request, user, to_email):
        mail_subject = "Confirma tu correo en calistopia"
        message = render_to_string(
            "email_templates/confirm_email.html",
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
        messages.success(request, f"El correo ha sido cambiado exitosamente.")
        return redirect("logout")
    else:
        return HttpResponse(
            "¡Link invalido!"
        )