# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

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
