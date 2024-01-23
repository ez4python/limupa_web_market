from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


# email sender service
def send_email(to_email, message):
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'Limupa Online Shopping'
    try:
        send_mail(subject, message, from_email, [to_email])
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    return HttpResponseRedirect("/contact/thanks/")
