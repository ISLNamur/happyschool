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
from core.models import StudentModel, TeachingModel, ResponsibleModel


class StudentAbsenceSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    sync_with_proeco = models.BooleanField("Synchronise les absences avec ProEco", default=False)


class JustificationModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    short_name = models.CharField("Nom court de la justification", max_length=20)
    name = models.CharField("Nom de la justification", max_length=200)
    date_just_start = models.DateField("Date de début de la justification")
    date_just_end = models.DateField("Date de fin de la justification")
    half_day_start = models.PositiveSmallIntegerField("Début demi-jour de la justification", default=0)
    half_day_end = models.PositiveSmallIntegerField("Fin de demi-jour de la justification", default=1)
    half_days = models.PositiveIntegerField("Nombre de demi-jour", default=0)


class StudentAbsenceModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_absence = models.DateField("Date de l'absence")
    morning = models.BooleanField("Matin", default=False)
    afternoon = models.BooleanField("Après-midi", default=False)
    username = models.CharField("Utilisateur qui a créé l'absence", max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
