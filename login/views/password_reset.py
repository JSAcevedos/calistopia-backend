from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from ..models import User

# Create and send reset link to email if user exists


def password_reset(request):
    if request.method == "GET":
        return render(request, "login_register/recover_page.html")
    else:
        try:
            user = (
                User.objects.get(email=request.POST["user"])
                if User.objects.filter(email=request.POST["user"]).exists()
                else User.objects.get(username=request.POST["user"])
            )
            sendEmail(request, user, user.email)
            messages.success(request, "Fue enviado un email de recuperacion al correo registrado, revisa la bandeja de spam.")
            return redirect("password_reset")
        except:
            messages.error(request, "El usuario no se encuentra registrado")
            return redirect("password_reset")


# If link is valid send reset form and check if form is valid for the user


def reset(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(id=uid)

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "GET":
            return render(request, "login_register/new_passw.html", {"uid": urlsafe_base64_encode(force_bytes(user.pk)), "token": token})
        else:
            if request.POST["new_password"] == request.POST["new_password2"]:

                user.set_password(request.POST["new_password"])
                user.save()
                messages.success(
                    request,
                    "La contraseña ha sido actualizada con exito, ya puedes ingresar a tu cuenta",
                )
            
                return redirect("login")
            else:
                messages.error(
                    request,
                    "Las contraseñas no coinciden",
                )
                return render(request, "login_register/new_passw.html", {"uid": urlsafe_base64_encode(force_bytes(user.pk)), "token": token})
    else:
        messages.error(
            request, "Link Invalido, solicita restablecer tu contraseña nuevamente"
        )
        return redirect("password_reset")


def sendEmail(request, user, to_email):
    mail_subject = "Restablece tu contraseña de Calistopia"
    message = render_to_string(
        "email_templates/pass_reset.html",
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
