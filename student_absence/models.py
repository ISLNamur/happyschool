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
from core.models import StudentModel, TeachingModel, ResponsibleModel, ClasseModel


class StudentAbsenceSettingsModel(models.Model):
    FILTER_NONE = "none"
    FILTER_BY_YEAR = "year"
    FILTER_BY_CLASS = "class"
    FILTER_CHOICES = [
        (FILTER_NONE, "No filter"),
        (FILTER_BY_YEAR, "Filter by year"),
        (FILTER_BY_CLASS, "Filter by class"),
    ]

    teachings = models.ManyToManyField(TeachingModel, default=None)
    sync_with_proeco = models.BooleanField("Synchronise les absences avec ProEco", default=False)
    filter_students_for_educ = models.CharField(max_length=5, choices=FILTER_CHOICES, default=FILTER_NONE)


class ClasseNoteModel(models.Model):
    classe = models.OneToOneField(ClasseModel, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    datetime_creation = models.DateTimeField("Date et heure de création de la note",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de la note",
                                           auto_now=True)


class JustificationModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    short_name = models.CharField("Nom court de la justification", max_length=20)
    name = models.CharField("Nom de la justification", max_length=200)
    date_just_start = models.DateField("Date de début de la justification")
    date_just_end = models.DateField("Date de fin de la justification")
    half_day_start = models.PositiveSmallIntegerField("Début demi-jour de la justification", default=0)
    half_day_end = models.PositiveSmallIntegerField("Fin de demi-jour de la justification", default=1)
    half_days = models.PositiveIntegerField("Nombre de demi-jour", default=0)


class PeriodModel(models.Model):
    """Model that describes a period of a day.

    Attributes:
        start Starting time of the period.
        end Ending time of the period.
        name Simple alias of the period.
    """
    start = models.TimeField()
    end = models.TimeField()
    name = models.CharField(max_length=200)
    day_of_week = models.CharField(max_length=10, default="1-5")

    @property
    def display(self):
        """Describe the period."""
        return "%s (%s-%s)" % (self.name, str(self.start)[:5], str(self.end)[:5])

    def __str__(self):
        return self.display


class StudentAbsenceModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_absence = models.DateField("Date de l'absence")
    period = models.ForeignKey(PeriodModel, on_delete=models.SET_NULL, null=True)
    is_absent = models.BooleanField("Étudiant absent", default=False)
    is_processed = models.BooleanField(default=False)
    username = models.CharField("Utilisateur qui a créé l'absence", max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
