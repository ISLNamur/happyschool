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

from core.models import TeachingModel, StudentModel, ResponsibleModel


class PIASettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel)


class DisorderModel(models.Model):
    disorder = models.CharField(max_length=1000)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.disorder


class DisorderResponseModel(models.Model):
    disorder = models.OneToOneField(DisorderModel, on_delete=models.CASCADE)
    response = models.CharField(max_length=1000)

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


class PIAModel(models.Model):
    """Main model for a PIA.
    A PIA is attached to a student and indenpendant of the student's year.
    """

    student = models.OneToOneField(StudentModel, on_delete=models.CASCADE)
    referent = models.ManyToManyField(ResponsibleModel, related_name="referent")
    sponsor = models.ManyToManyField(ResponsibleModel, related_name="sponsor")
    disorder = models.ManyToManyField(DisorderModel)
    disorder_response = models.ManyToManyField(DisorderResponseModel)
    schedule_adjustment = models.ManyToManyField(ScheduleAdjustmentModel)

    def __str__(self):
        """String representation of the PIAModel, return the student's description."""
        return str(self.student)


class CrossGoalModel(models.Model):
    goal = models.CharField(max_length=200)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.goal


class BranchModel(models.Model):
    branch = models.CharField(max_length=200)
    teachings = models.ManyToManyField(TeachingModel)

    def __str__(self):
        return self.branch


class BranchGoalModel(models.Model):
    goal = models.CharField(max_length=200)
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE)

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


class GoalModel(models.Model):
    pia_model = models.ForeignKey(PIAModel, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    cross_goals = models.CharField(max_length=2000)
    given_help = models.CharField(max_length=1000)
    responsible = models.ManyToManyField(ResponsibleModel, blank=True)
    self_assessment = models.CharField(max_length=2000)
    assessment = models.ForeignKey(AssessmentModel, on_delete=models.SET_NULL, null=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)


class SubGoalModel(models.Model):
    goal = models.ForeignKey(GoalModel, on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchModel, on_delete=models.SET_NULL, null=True)
    branch_goals = models.CharField(max_length=2000)
    given_help = models.CharField(max_length=1000)
    self_assessment = models.CharField(max_length=2000)
    assessment = models.ForeignKey(AssessmentModel, on_delete=models.SET_NULL, null=True)
    parent_commitment = models.CharField(max_length=2000)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_update = models.DateTimeField(auto_now=True)
