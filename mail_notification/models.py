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

import string
import random
from time import strftime

from django.db import models
from django.contrib.auth.models import Group

from mail_answer.models import MailTemplateModel


def unique_file_name(instance, filename):
    path = strftime('attachments/%Y/%m/%d/')
    file = "".join(random.choice(string.ascii_letters) for x in range(0, 8)) + "_" + filename
    return path + file

class EmailAttachment(models.Model):
    attachment = models.FileField(upload_to=unique_file_name)


class EmailSender(models.Model):
    sender_email = models.EmailField()
    sender_email_name = models.CharField(max_length=100)
    groups = models.ManyToManyField(Group)
    teaching = models.CharField(max_length=30)

    def __str__(self):
        return "%s (%s)" % (self.sender_email_name, self.sender_email)


class EmailTag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class EmailNotification(models.Model):
    email_to = models.CharField(max_length=500)
    email_from = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    errors = models.CharField(max_length=4000)
    attachments = models.ManyToManyField(EmailAttachment)
    tags = models.ManyToManyField(EmailTag)
    teaching = models.CharField(max_length=50)
    answers = models.ForeignKey(MailTemplateModel, on_delete=models.SET_NULL, null=True)
    datetime_created = models.DateTimeField("Date de création")

    def __str__(self):
        return """
        to: %s
        from: %s
        subject: %s
        body: %s
        attachments: %i
        teaching: %s
        """ % (self.email_to, self.email_from, self.subject, self.body[:40], len(self.attachments.all()), self.teaching)

    class Meta:
        permissions = (
            ('access_mail_notification', 'Can access to mail notification'),
        )


class OtherEmailGroupModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class OtherEmailModel(models.Model):
    email = models.EmailField()
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    group = models.ForeignKey(OtherEmailGroupModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.email + '(%s)' % str(self.group)
