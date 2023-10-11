from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from ..tokens import account_activation_token
from django.db import IntegrityError
from smtplib import SMTPRecipientsRefused
from ..models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound
from django.http import HttpResponse


def signup(request):
    if request.method == "GET":
        return HttpResponseNotFound("<h1>Not Found<h1>")
    else:
        try:
            if request.POST["password"] == request.POST["confirm-password"]:
                user = User(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                )
                user.password = make_password(
                    user.password, salt=None, hasher="default"
                )
                user.save()
                activateEmail(request, user, user.email)
                messages.success(request, '¡Cuenta creada! ¡Porfavor revisa tu correo para activar tu cuenta de Calistopia!')
                return redirect("index")
            else:
                messages.success(request, 'Las contraseñas no coincide')
                return redirect("index")
        except IntegrityError:
            messages.success(request, 'El usuario ya existe')
            return redirect("index")

        except SMTPRecipientsRefused:
            user.delete()
            messages.success(request, 'El correo electrónico no es valido')
            return redirect("index")


# Send activation email


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "activationEmail.html",
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
            "Link invalido, por favor resgistrate nuevamente para obtener un nuevo link."
            )
        return HttpResponse(
            "¡Link invalido!"
        )
