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
from django.contrib.auth.models import Group
from django.utils import timezone

from core.models import EmailModel, StudentModel, ResponsibleModel, TeachingModel


class AppelsSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)


class MotiveModel(models.Model):
    display = models.CharField(max_length=200)

    def __str__(self):
        return self.display


class ObjectModel(models.Model):
    display = models.CharField(max_length=200)

    def __str__(self):
        return self.display


class Appel(models.Model):
    matricule = models.ForeignKey(
        StudentModel,
        on_delete=models.SET_NULL,
        to_field="matricule",
        null=True,
        blank=True,
        default=None,
    )
    responsible = models.ForeignKey(
        ResponsibleModel, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    name = models.CharField(max_length=100)
    is_student = models.BooleanField(default=True)
    user = models.CharField(max_length=100, default="")
    objet = models.CharField(max_length=300)  # DEPRECATED, use object instead.
    motif = models.CharField(max_length=300)  # DEPRECATED, use motive instead.
    object = models.ForeignKey(ObjectModel, on_delete=models.CASCADE, null=True, blank=True)
    motive = models.ForeignKey(MotiveModel, on_delete=models.CASCADE, null=True, blank=True)
    datetime_motif_start = models.DateTimeField(
        "Début date d'appel", null=True, default=None
    )  # DEPRECATED
    date_motif_start = models.DateField(null=True)
    time_motif_start = models.TimeField("Début heure d'appel", null=True, default=None)
    datetime_motif_end = models.DateTimeField(
        "Fin date d'appel", null=True, default=None
    )  # DEPRECATED
    date_motif_end = models.DateField(null=True)
    time_motif_end = models.TimeField(null=True)
    datetime_appel = models.DateTimeField("Date d'appel")
    commentaire = models.CharField(max_length=2000, blank=True)
    traitement = models.CharField(max_length=2000, null=True, blank=True)
    datetime_traitement = models.DateTimeField("Date traitement", null=True, blank=True)
    is_traiter = models.BooleanField()
    emails = models.ManyToManyField(EmailModel, blank=True)
    custom_email = models.EmailField(default=None, blank=True, null=True)
    datetime_encodage = models.DateTimeField("Date d'encodage", default=timezone.now)
