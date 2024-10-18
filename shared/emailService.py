from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.exceptions import APIException

from config import settings


class EmailSendException(APIException):
    status_code = 500
    default_detail = 'Failed to send email.'
    default_code = 'email_send_failed'


def send_email(token, email):
    token_link = settings.FRONT_URL + "/invoices/" + str(token) + "/ "

    try:
        subject = 'Your Access Token'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        html_content = render_to_string('sendToken.html', {'email': email, 'url': token_link})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        raise EmailSendException() from e
