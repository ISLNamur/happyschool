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
from django.contrib.auth.models import User, Group

from core.models import StudentModel, TeachingModel, ResponsibleModel, ClasseModel

class StudentAbsenceTeacherSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    can_see_list = models.ManyToManyField(Group, default=None, blank=True, related_name="can_see_list")


class LessonModel(models.Model):
    lesson = models.CharField(max_length=200)
    classe = models.ForeignKey(ClasseModel, on_delete=models.CASCADE)


class PeriodModel(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    name = models.CharField(max_length=200)

    @property
    def display(self):
        return "%s (%s-%s)" % (self.name, str(self.start)[:5], str(self.end)[:5])


class StudentAbsenceTeacherModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_absence = models.DateField(auto_now=True)
    lesson = models.ForeignKey(LessonModel, on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey(PeriodModel, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
                                

class StudentLatenessTeacherModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_lateness = models.DateField(auto_now=True)
    lesson = models.ForeignKey(LessonModel, on_delete=models.SET_NULL, null=True)
    period = models.ForeignKey(PeriodModel, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
