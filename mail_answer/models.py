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

import uuid

from django.db import models

from core.models import StudentModel


class MailAnswerSettingsModel(models.Model):
    use_remote = models.BooleanField(default=False)
    is_remote = models.BooleanField(default=False)
    remote_url = models.URLField(default="http://localhost/")


class ChoiceModel(models.Model):
    text = models.CharField(max_length=500)
    input = models.BooleanField(default=False)


class OptionModel(models.Model):
    text = models.CharField(max_length=500)
    input = models.BooleanField(default=False)


class MailTemplateModel(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    acknowledge = models.BooleanField()
    acknowledge_text = models.CharField(
        max_length=500, default="Je déclare avoir pris connaissance des présentes informations."
    )
    choices = models.ManyToManyField(ChoiceModel, blank=True)
    options = models.ManyToManyField(OptionModel, blank=True)
    is_used = models.BooleanField(default=False)
    datetime_creation = models.DateTimeField()


class MailAnswerModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    template = models.ForeignKey(
        MailTemplateModel, on_delete=models.CASCADE, default=None, null=True
    )
    answers = models.JSONField(default=dict)
    is_answered = models.BooleanField(default=False)
