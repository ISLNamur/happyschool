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

from datetime import date

from django.db import models
from django.contrib.auth.models import Group

from core.models import StudentModel, TeachingModel, YearModel, ClasseModel


class LatenessSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    printer = models.CharField(
        max_length=200,
        blank=True,
        help_text='IP address of one or multiple printers. If multiple, it must be separated by a comma ","',
    )
    date_count_start = models.DateField(default=date(year=2019, month=9, day=1))
    notify_responsible = models.BooleanField(default=False)
    enable_camera_scan = models.BooleanField(default=False)
    use_email_school = models.BooleanField(default=False)


class SanctionTriggerModel(models.Model):
    WEEK_DAY_CHOICES = [
        (None, "Choisir un jour de la semaine"),
        (1, "Lundi"),
        (2, "Mardi"),
        (3, "Mercredi"),
        (4, "Jeudi"),
        (5, "Vendredi"),
        (6, "Samedi"),
        (7, "Même jour"),
    ]
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    sanction_id = models.PositiveIntegerField(null=True, blank=True)
    lateness_count_trigger_first = models.PositiveSmallIntegerField(default=4)
    lateness_count_trigger = models.PositiveSmallIntegerField(default=3)
    year = models.ManyToManyField(YearModel, blank=True)
    classe = models.ManyToManyField(ClasseModel, blank=True)
    only_warn = models.BooleanField(default=False)
    next_week_day = models.PositiveSmallIntegerField(
        choices=WEEK_DAY_CHOICES, null=True, blank=True
    )
    delay = models.PositiveSmallIntegerField(
        default=1,
        help_text="""Le nombre de jour avant de postposer la sanction à la semaine d'après.
        Par exemple, pour une valeur de 1, si le retard qui déclenche la sanction a lieu
        le même jour de la semaine que la sanction, la sanction sera mise la semaine prochaine
        parce qu'il y a moins de 1 jour de différence. Au contraire, si le retard à lieu 1 jour
        avant le jour de sanction, la sanction sera mise le lendemain.""",
        null=True,
        blank=True,
    )
    time_lateness_start = models.TimeField(
        null=True, blank=True, help_text="Début de l'interval du retard (facultatif)."
    )
    time_lateness_stop = models.TimeField(
        null=True,
        blank=True,
        help_text="Fin de l'interval du retard (facultatif si le début de l'interval n'est pas précisé).",
    )
    sanction_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.WEEK_DAY_CHOICES[self.next_week_day][1]} tous les {self.lateness_count_trigger} retards ({self.id})"


class LatenessModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, null=True)
    has_sanction = models.BooleanField(default=False)
    sanction_id = models.PositiveIntegerField(null=True, blank=True)
    justified = models.BooleanField(default=False)
    datetime_creation = models.DateTimeField(
        "Date et heure de création du retard", auto_now_add=True
    )
    datetime_update = models.DateTimeField("Date et heure de mise à jour du retard", auto_now=True)

    @property
    def lateness_count(self):
        settings = LatenessSettingsModel.objects.first()
        return LatenessModel.objects.filter(
            student=self.student, justified=False, datetime_creation__gte=settings.date_count_start
        ).count()


class MailTemplateModel(models.Model):
    name = models.CharField(max_length=100, default="warning")
    template = models.TextField()
