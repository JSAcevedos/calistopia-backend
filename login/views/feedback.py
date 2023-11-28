from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from ..models import Feedback
from django.http import Http404

@login_required
def feedback(request):
    try:
        pqr = request.POST["type"]
        content = request.POST["feedback"]
        feedback = Feedback.objects.create_feedback(request.user.id, pqr, content)
        messages.info(request,f"Tú y nuestros administradores han recibido un correo con tu {pqr}.")
        send_email(request, feedback)
    except MultiValueDictKeyError:
        pass
    return render(request, "feedback/feedback.html")

@login_required
def user_feedback(request):
    queryset = Feedback.objects.filter(user_id = request.user.id)
    objects = queryset.all()
    context = {"feedback": [objects]}
    return render(request, "feedback/user_feedback.html", context)

@login_required
def feedback_content(request, fid):
    try:
        feedback = Feedback.objects.get(feedback_id = fid)
        if feedback.user_id == request.user.id  or request.user.is_admin:
            context = {"feedback": feedback}
            return render(request, "feedback/feedback_content.html", context = context)
        else:
            return redirect(request, "user_feedback")
    except:
        raise Http404

@login_required
def delete_feedback(request, fid):
    try:
        feedback = Feedback.objects.get(feedback_id = fid)
        if feedback.user_id == request.user.id:
            messages.info(request, f"{feedback.feedback_type} eliminada satisfactoriamente.")
            feedback.delete()
        else:
            messages.info(request, f"Algo ha salido mal, intentalo nuevamente.")
        return redirect("user_feedback")
    except:
        raise Http404

def send_email(request, feedback):
    admin_mail_subject = f"Feedback Calistopia - Usuario {request.user.username}"
    user_mail_subject = f"Calistopia - {feedback.feedback_type} realizada con éxito"
    admin_message = f"El usuario {request.user.username} ha realizado una {feedback.feedback_type.lower()} a través del módulo de feedback. El usuario ha enviado la siguiente {feedback.feedback_type.lower()} con id {feedback.feedback_id}:\n {feedback.content}"
    user_message =  render_to_string(
            "email_templates/user_feedback.html",
            {
                "user": request.user.username,
                "domain": request.get_host,
                "type": feedback.feedback_type,
                "id": feedback.feedback_id,
                "protocol": "https" if request.is_secure() else "http",
            },
        )
    user_email = EmailMultiAlternatives(user_mail_subject, user_message, to=[request.user.email], bcc=["calistopia2023@gmail.com"])
    admin_email = EmailMessage(admin_mail_subject, admin_message, to=["calistopia2023@gmail.com"])
    user_email.send()
    admin_email.send()

@login_required
def actualice_feedback(request, fid):
    try:
        if request.user.is_admin:
            feedback = Feedback.objects.get(feedback_id=fid)
            respuesta = request.POST["respuesta"]

            new_content = feedback.content + "\n\n***Respuesta de los administradores***\n\n" + respuesta

            #feedback.content = "El back lever no es de espalda."
            feedback.content = new_content
            feedback.state = True
            feedback.save()

        return redirect(f"/user_feedback/{fid}/")
    except:
        raise Http404
