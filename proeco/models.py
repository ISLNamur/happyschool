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

from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder

from core.models import TeachingModel

people_type = [("student", "Étudiant"), ("responsible", "Responsable")]


class OverwriteDataModel(models.Model):
    people = models.CharField(max_length=20, choices=people_type)
    uid = models.BigIntegerField(
        help_text="Identifiant unique (matricule de l'étudiant ou du responsable).",
        null=True,
        blank=True,
    )
    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    old_value = models.CharField(max_length=100, blank=True)


class TemplateSelectionModel(models.Model):
    template = models.TextField()


class ProEcoWriteModel(models.Model):
    WAITING = "waiting"
    DONE = "done"
    ERROR = "error"
    STUDENT = "stud"
    RESPONSIBLE = "resp"

    STATUS_CHOICES = [
        (WAITING, "Waiting"),
        (DONE, "Done"),
        (ERROR, "Error"),
    ]

    PERSON_CHOICES = [
        (STUDENT, "Student"),
        (RESPONSIBLE, "Responsible"),
    ]

    app = models.CharField(max_length=100)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    payload = models.JSONField(encoder=DjangoJSONEncoder)
    method = models.CharField(max_length=30)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=WAITING)
    person = models.CharField(max_length=4, choices=PERSON_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.deletion.SET_NULL)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str((self.datetime_creation, self.app, self.method, self.status))
