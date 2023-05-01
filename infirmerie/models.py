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
from core.models import StudentModel, TeachingModel


class InfirmerieSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class Passage(models.Model):
    matricule = models.ForeignKey(
        StudentModel, on_delete=models.SET_NULL, to_field="matricule", null=True, blank=True
    )
    name = models.CharField(max_length=100)
    datetime_arrive = models.DateTimeField("date d'arrivée")
    datetime_sortie = models.DateTimeField("date de sortie", null=True, blank=True)
    motifs_admission = models.CharField(max_length=2000)
    remarques_sortie = models.CharField(max_length=2000, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(datetime_sortie__isnull=True)
                    | models.Q(datetime_sortie__gte=models.F("datetime_arrive"))
                ),
                name="correct_datetime",
            )
        ]
