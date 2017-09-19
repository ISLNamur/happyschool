import os

from django.core.mail import EmailMultiAlternatives, get_connection
# from django.core.mail.backends.smtp import
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from email.mime.image import MIMEImage
from .models import EmailModel


def send_email(to, subject, email_template, cc=None, images=None, context=None):
    connection = get_connection()
    html_content = render_to_string(email_template, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to, cc, connection)
    email.attach_alternative(html_content, "text/html")

    if images:
        email.mixed_subtype = 'related'
        for i in images:
            #email.headers()
            image_name = i.split("/")[-1]
            fp = open(settings.BASE_DIR + i, 'rb')
            msg_img = MIMEImage(fp.read())
            msg_img.add_header('Content-Id', '<' + image_name + '>')
            email.attach(msg_img)
            fp.close()
            
    email.send()

def get_resp_emails(student):
    emails = {}
    for e in EmailModel.objects.filter(teaching=student.teaching, years=student.classe.year):
        emails[e.email] = e.display

    return emails
