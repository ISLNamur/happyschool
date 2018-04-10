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


class ScheduleChange(models.Model):
    date_start = models.DateField("Date de début")
    date_end = models.DateField("Date de fin", null=True, blank=True) # TODO Need (can be the same day)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    classes = models.CharField(default="", blank=True, max_length=100)
    activity = models.CharField(default="", blank=True, max_length=500)
    teachers = models.CharField(default="", blank=True, max_length=500)
    place = models.CharField(default="", blank=True, max_length=200)
    comment = models.CharField(default="", blank=True, max_length=500)
    datetime_encodage = models.DateTimeField("Date d'encodage")
    user = models.CharField(default="", blank=True, max_length=100)

    class Meta:
        ordering = ('date_start', 'time_start')
