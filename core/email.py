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
from typing import Callable, Optional, Sequence
import requests

from django.core.mail import EmailMultiAlternatives, get_connection

# from django.core.mail.backends.smtp import
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.fields.files import FieldFile

from email.mime.image import MIMEImage
from .models import EmailModel, StudentModel, ResponsibleModel
from core.views import get_core_settings


EMAIL_PROVIDER_SWEEGO: str = "sweego"


def send_with_other_provider(email: EmailMultiAlternatives) -> int:
    if settings.OTHER_EMAIL_PROVIDER == EMAIL_PROVIDER_SWEEGO:
        # DO NOT SUPPORT ATTACHMENTS (images and files).
        payload = {
            "channel": "email",
            "provider": "sweego",
            "recipients": [{"email": r} for r in email.recipients()],
            "from": email.from_email,
            "subject": email.subject,
            "message-txt": email.body,
            "reply-to": [{"email": r} for r in email.reply_to],
        }

        html_text = [alt.content for alt in email.alternatives if alt.mimetype == "text/html"]
        if html_text:
            payload["message-html"] = html_text[0]

        URL = "https://api.sweego.io/send"
        headers = {
            "Api-Key": settings.SWEEGO_API,
            "Content-Type": "application/json",
        }

        TIMEOUT = 10
        response = requests.post(URL, json=payload, headers=headers, timeout=TIMEOUT)

        # Check the response status code
        if response.status_code == 200:
            return 1
        else:
            print(response.json())
            return 0

    raise ValueError(
        f"OTHER_EMAIL_PROVIDER {settings.OTHER_EMAIL_PROVIDER} not supported. See docs for available provider"
    )


def send_email(
    to: Sequence[str],
    subject,
    email_template: Optional[str] = None,
    body: str | None = None,
    cc: Sequence[str] | None = None,
    images: Sequence[str] | None = None,
    context: dict | None = None,
    attachments=None,
    use_bcc: bool = False,
    reply_to: str | None = None,
    from_email: str | None = None,
    clean_from_email: Callable[[str], str] | None = None,
    clean_reply_to: Callable[[Sequence], Sequence] | None = None,
) -> bool:
    """
    Send an email

    :param images: A sequence of path to images.
    :param attachments: A sequence of FileField.
    """

    to: list[str] = list(to)
    if not to:
        return False

    if email_template:
        # Auto include core_settings.
        if not context:
            context = {"core_settings": get_core_settings()}
        elif not "core_settings" in context:
            context = {"core_settings": get_core_settings()} | context

        html_content = render_to_string(template_name=email_template, context=context)
        text_content = strip_tags(html_content)
    elif body:
        html_content = body
        text_content = strip_tags(body)
    else:
        raise ValueError("A template or a body have to be provided")

    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    if clean_from_email:
        from_email = clean_from_email(from_email)

    if clean_reply_to:
        reply_to = clean_reply_to(reply_to)

    connection = get_connection()
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to,
        cc=cc,
        connection=connection,
        reply_to=reply_to,
    )
    if use_bcc:
        email.to = []
        email.bcc = to
    email.attach_alternative(html_content, "text/html")

    if images:
        email.mixed_subtype = "related"
        for i in images:
            # email.headers()
            image_name = i.split("/")[-1]
            fp = open(str(settings.BASE_DIR) + i, "rb")
            msg_img = MIMEImage(fp.read())
            msg_img.add_header("Content-Id", "<" + image_name + ">")
            email.attach(msg_img)
            fp.close()
    if attachments:
        for a in attachments:
            if isinstance(a, dict):
                email.attach(filename=a["filename"], content=a["file"])
            elif isinstance(a.attachment, FieldFile):
                email.attach_file(a.attachment.path)

    response = False
    if settings.DEBUG or not settings.EMAIL_HOST or settings.EMAIL_HOST == "smtp.server.com":
        if settings.EMAIL_ADMIN:
            email.to = [settings.EMAIL_ADMIN]
            if OTHER_EMAIL_PROVIDER in settings:
                response = send_with_other_provider(email)
            else:
                response = email.send()
        else:
            print(email.body)
    else:
        if OTHER_EMAIL_PROVIDER in settings:
            response = send_with_other_provider(email)
        else:
            response = email.send()

    return response > 0


def get_resp_emails(student: StudentModel) -> dict:
    """Return a dict of emails and names of responsible that are in charge of the student."""
    emails = {}
    for e in EmailModel.objects.filter(teaching=student.teaching, years=student.classe.year):
        emails[e.email] = e.display

    # Get educators that are related by classes to the student.
    educators = ResponsibleModel.objects.filter(
        teaching=student.teaching, classe=student.classe, is_educator=True
    )
    emails = dict(emails, **{e.email_school: e.fullname for e in educators})

    return emails
