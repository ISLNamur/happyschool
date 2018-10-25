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
from django.contrib.auth.models import Group, User
from core.models import TeachingModel, EmailModel, ResponsibleModel


class ScheduleChangeSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    notify_by_email_to = models.ManyToManyField(EmailModel)
    email_school = models.BooleanField(default=False)


class ScheduleChangeModel(models.Model):
    change = models.CharField(max_length=100)
    date_change = models.DateField("Date")
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    classes = models.CharField(default="", blank=True, max_length=100)
    teachers_replaced = models.ManyToManyField(ResponsibleModel, related_name="teachers_replaced")
    teachers_substitute = models.ManyToManyField(ResponsibleModel, related_name="teachers_substitute", blank=True)
    place = models.CharField(default="", blank=True, max_length=200)
    comment = models.CharField(default="", blank=True, max_length=500)
    datetime_created = models.DateTimeField("date d'encodage", auto_now_add=True)
    datetime_modified = models.DateTimeField("Date de modification", auto_now=True)
    user = models.CharField(default="", blank=True, max_length=100)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('access_schedule_change', 'Can access to schedule change data'),
        )
