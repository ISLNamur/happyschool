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

import random
import string

from time import strftime

from django.db import models
from django.contrib.auth.models import Group

from core.models import TeachingModel, StudentModel, ResponsibleModel


def unique_file_name(instance, filename):
    path = strftime('pia/%Y/%m/%d/')
    file = "".join(random.choice(string.ascii_letters) for x in range(0, 3)) + "_" + filename
    return path + file


class PIASettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    filter_teacher_entries_by_tenure = models.BooleanField(
        default=False,
        help_text="""
        Si activé, seuls les titulaires peuvent voir les PIA de leurs élèves.
        Sinon sera limité aux classes associées.
        """
    )
    weekday_support_activity = models.CharField(
        max_length=20, default="1-5", help_text="""Jour de la semaine où il y activité de support.
        Spécifier les jours par intervalles avec un tiret ('1-5' pour du lundi au vendredi)
        et par virgule pour des jours distincts ('1,3,5' pour lundi, mercredi, vendredi).
        Peut être une combinaison des deux."""
    )


class AttachmentModel(models.Model):
    attachment = models.FileField(upload_to=unique_file_name)


class DisorderModel(models.Model):
    disorder = models.CharField(max_length=1000)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.disorder


class DisorderResponseCategoryModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DisorderResponseModel(models.Model):
    disorder = models.ForeignKey(DisorderModel, on_delete=models.CASCADE)
    response = models.CharField(max_length=1000)
    categories = models.ManyToManyField(DisorderResponseCategoryModel)

    def __str__(self):
        return "%s (%s)" % (self.response, self.disorder)


class ScheduleAdjustmentModel(models.Model):
    """Adjustment made in the student's schedule.

    Attributes:
        schedule_adjustment Description of the schedule adjustment.
    """

    schedule_adjustment = models.CharField(
        max_length=200,
        help_text="Description de l'aménagement horaire"
    )

    def __str__(self):
        return self.schedule_adjustment


class PIAModel(models.Model):
    """Main model for a PIA.
    A PIA is attached to a student and indenpendant of the student's year.
    """

    student = models.OneToOneField(StudentModel, on_delete=models.CASCADE)
    referent = models.ManyToManyField(ResponsibleModel, related_name="referent")
    sponsor = models.ManyToManyField(ResponsibleModel, related_name="sponsor")
    disorder = models.ManyToManyField(DisorderModel, blank=True)
    disorder_response = models.ManyToManyField(DisorderResponseModel, blank=True)
    schedule_adjustment = models.ManyToManyField(ScheduleAdjustmentModel, blank=True)
    other_adjustments = models.TextField(blank=True)
    attachments = models.ManyToManyField(AttachmentModel, blank=True)
    advanced = models.BooleanField(default=True)
    support_activities = models.JSONField(default=dict)

    def __str__(self):
        """String representation of the PIAModel, return the student's description."""
        return str(self.student)


class StudentProjectModel(models.Model):
    pia_model = models.ForeignKey(PIAModel, on_delete=models.CASCADE)
    student_project = models.TextField()
    date_student_project = models.DateField()
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class ParentsOpinionModel(models.Model):
    pia_model = models.ForeignKey(PIAModel, on_delete=models.CASCADE)
    parents_opinion = models.TextField()
    date_parents_opinion = models.DateField()
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class CrossGoalItemModel(models.Model):
    goal = models.CharField(max_length=200)
    advanced = models.BooleanField(default=True)
    basic = models.BooleanField(default=False)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.goal


class BranchModel(models.Model):
    branch = models.CharField(max_length=200)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.branch


class BranchGoalItemModel(models.Model):
    goal = models.CharField(max_length=200)
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE, null=True, blank=True)
    advanced = models.BooleanField(default=True)
    basic = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.goal, self.branch)


class AssessmentModel(models.Model):
    """Assessment model of a goal (cross goal or branch goal).

        Attributes:
            assessment Description of the assessment.
    """

    assessment = models.CharField(
        max_length=200,
        help_text="Description de l'évaluation."
    )

    """String representation of the AssessmentModel, return the description of
    the assessment."""
    def __str__(self):
        return self.assessment


class BaseGoal(models.Model):
    pia_model = models.ForeignKey(PIAModel, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    indicator_action = models.TextField(blank=True)
    given_help = models.TextField(blank=True)
    responsible = models.ManyToManyField(ResponsibleModel, blank=True)
    self_assessment = models.CharField(max_length=2000, blank=True)
    assessment = models.ForeignKey(AssessmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    validated = models.BooleanField(default=False)
    attachments = models.ManyToManyField(AttachmentModel, blank=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-date_end", "-date_start",]


class CrossGoalModel(BaseGoal):
    cross_goals = models.CharField(max_length=2000)
    branches = models.ManyToManyField(BranchModel, blank=True)

    def cross_goals_list(self):
        return self.cross_goals.split(";")


class BranchGoalModel(BaseGoal):
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE)
    branch_goals = models.CharField(max_length=2000)
    parent_commitment = models.TextField(blank=True)

    def branch_goals_list(self):
        return self.branch_goals.split(";")


class ClassCouncilPIAModel(models.Model):
    """Class council model. A class council happens at a specific
    date and makes a statement for each branch of the progress and
    difficulties.
    """

    pia_model = models.ForeignKey(PIAModel, on_delete=models.CASCADE)
    date_council = models.DateField()
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class OtherStatementModel(models.Model):
    """Free Statement from a class council for a specific branch."""

    class_council = models.ForeignKey(ClassCouncilPIAModel, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE)
    resources = models.TextField(blank=True)
    difficulties = models.TextField(blank=True)
    others = models.TextField(blank=True)


class ResourceDifficultyModel(models.Model):
    resource = models.CharField(max_length=300)
    difficulty = models.CharField(max_length=300)
    category = models.CharField(max_length=300, blank=True)
    advanced = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.resource} <-> {self.difficulty}"


class StudentStateModel(models.Model):
    """States the resources and difficulties of the student at a class council."""

    class_council = models.ForeignKey(ClassCouncilPIAModel, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE, null=True, blank=True)
    resources = models.ManyToManyField(
        ResourceDifficultyModel, blank=True, related_name="resources"
    )
    difficulties = models.ManyToManyField(
        ResourceDifficultyModel, blank=True, related_name="difficulties"
    )
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class LogPIAModel(models.Model):
    log = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.datetime} - {self.log}"
