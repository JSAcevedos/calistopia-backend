from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.http import HttpResponseNotFound
from smtplib import SMTPRecipientsRefused
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from ..models import User


def signup(request):
    if request.method == "GET":
        return HttpResponseNotFound("<h1>Not Found<h1>")
    else:
        try:
            if request.POST["password"] == request.POST["confirm-password"]:
                user = User.objects.create_user(
                    request.POST["username"], 
                    request.POST["password"], 
                    request.POST["email"]
                )
                activateEmail(request, user, user.email)
                messages.success(request, '¡Cuenta creada! ¡Porfavor revisa tu correo para activar tu cuenta de Calistopia!') 
                return redirect("login")
            else:
                messages.error(request, 'Las contraseñas no coincide')
                return redirect("login")
        except IntegrityError:
            messages.error(request, 'El usuario ya existe')
            return redirect("login")

        except SMTPRecipientsRefused:
            user.delete()
            messages.error(request, 'El correo electrónico no es valido')
            return redirect("login")


# Send activation email


def activateEmail(request, user, to_email):
    mail_subject = "Activa tu cuenta de Calistopia"
    message = render_to_string(
        "activation_email.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


# Activation view


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        return HttpResponse(
            "Gracias por la confirmación, ya puedes ingresar a tu cuenta!"
        )
    else:
        if not user.active:
            user.delete()
            return HttpResponse(
            "Link invalido, por favor registrate nuevamente para obtener un nuevo link."
            )
        return HttpResponse(
            "¡Link invalido!"
        )