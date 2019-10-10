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
    responsible_phone = models.CharField(max_length=30, default="")
    responsible_name = models.CharField(max_length=100, default="")
    email_school = models.BooleanField(default=False)
    copy_to_remote = models.BooleanField(default=False, help_text="Copie toutes les entrées créées "
                                                                  "sur le serveur distant (remote)."
                                                                  "Le serveur distant doit être"
                                                                  "configuré dans CoreSettingsModel")


class ScheduleChangeTypeModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ScheduleChangeCategoryModel(models.Model):
    category = models.CharField(max_length=100)
    color = models.CharField(default="", max_length=6, help_text="Valeur hexadecimal de la couleur.")
    icon = models.CharField(default="", max_length=50, help_text="Icône utilisée par Font Awesome 4.7.")

    def __str__(self):
        return "%s %s" % (self.category, self.color,)


class ScheduleChangePlaceModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ScheduleChangeModel(models.Model):
    change = models.ForeignKey(ScheduleChangeTypeModel, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ScheduleChangeCategoryModel, on_delete=models.SET_NULL, blank=True, null=True)
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

    def __str__(self):
        return "%s (%s-%s): %s" % (self.date_change,
                                   self.time_start.strftime("%H:%M") if self.time_start else "-",
                                   self.time_end.strftime("%H:%M") if self.time_end else "-",
                                   self.change.name,)
