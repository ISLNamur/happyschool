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

from dateutil.relativedelta import relativedelta

from django.utils import timezone
from django.db import models

from core.models import TeachingModel, EmailModel


class AbsenceProfSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    emails = models.ManyToManyField(EmailModel, default=None)


class MotifAbsence(models.Model):
    motif = models.CharField(max_length=200)

    def __str__(self):
        return self.motif


class Absence(models.Model):
    id_person = models.BigIntegerField(blank=True, null=True, default=None)
    name = models.CharField(max_length=500)
    motif = models.CharField(max_length=500)
    datetime_absence_start = models.DateTimeField("date du début de l'absence", null=True, blank=True)
    date_absence_start = models.DateField("Date du début de l'absence", default=timezone.now().today())
    datetime_absence_end = models.DateTimeField("date de la fin de l'absence", null=True, blank=True)
    date_absence_end = models.DateField("Date de la fin de l'absence", default=timezone.now().today())
    datetime_encoding = models.DateTimeField("date de l'encodage", auto_now_add=True)
    comment = models.CharField(max_length=10000, blank=True)
    user = models.CharField(max_length=20)

    class Meta:
        permissions = (
            ('access_absences', 'Can access to absences data'),
        )

    @property
    def status(self):
        if (self.date_absence_start < timezone.now().date()
                and self.date_absence_end > timezone.now().date() - relativedelta(days=1)):
            return "En cours"

        if self.date_absence_start > timezone.now().date():
            return "A venir"

        return "Clôturé"
