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

from django.conf import settings

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.serializers import StudentSerializer, GivenCourseSerializer
from core.models import StudentModel, GivenCourseModel

from .models import (
    StudentAbsenceTeacherSettingsModel,
    StudentAbsenceTeacherModel,
    StudentAbsenceEducModel,
    PeriodModel,
    PeriodEducModel,
    JustMotiveModel,
    JustificationModel,
)


class StudentAbsenceTeacherSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAbsenceTeacherSettingsModel
        fields = "__all__"


class PeriodTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodModel
        fields = ("id", "name", "start", "end", "display", "day_of_week")


class PeriodEducSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodEducModel
        fields = "__all__"


class JustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustificationModel
        fields = "__all__"

        validators = [
            UniqueTogetherValidator(
                queryset=JustificationModel.objects.all(),
                fields=[
                    "date_just_start",
                    "date_just_end",
                    "half_day_start",
                    "half_day_end",
                    "student",
                ],
                message="Une justification existe déjà pour cet étudiant à cette période. Actualisez la page pour mettre les données à jour.",
            )
        ]

    def validate(self, data):
        # Check if there is already an overlapping justification.

        # Look for dates interval intersections.
        for just in JustificationModel.objects.filter(
            date_just_start__lte=data["date_just_end"],
            date_just_end__gte=data["date_just_start"],
            student=data["student"],
        ):
            # Don't compare with itself.
            if self.instance and self.instance.id == just.id:
                continue

            # On the edge of the interval.
            if (
                data["date_just_start"] < just.date_just_start
                and data["date_just_end"] == just.date_just_start
                and data["half_day_end"] < just.half_day_start
            ):
                continue
            if (
                data["date_just_end"] >= just.date_just_end
                and data["date_just_start"] == just.date_just_end
                and data["half_day_start"] > just.half_day_end
            ):
                continue

            raise serializers.ValidationError(
                "Il existe déjà une justification pour cet étudiant à cette période."
            )

        return data


class JustMotiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustMotiveModel
        fields = "__all__"


class StudentAbsenceTeacherSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields: field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentModel.objects.all(), source="student", required=False, allow_null=True
    )

    given_course = GivenCourseSerializer(read_only=True)
    given_course_id = serializers.PrimaryKeyRelatedField(
        queryset=GivenCourseModel.objects.all(),
        source="given_course",
        required=False,
        allow_null=True,
    )

    period = PeriodTeacherSerializer(read_only=True)
    period_id = serializers.PrimaryKeyRelatedField(
        queryset=PeriodModel.objects.all(), source="period", required=False, allow_null=True
    )

    class Meta:
        model = StudentAbsenceTeacherModel
        fields = [
            "id",
            "student",
            "student_id",
            "given_course",
            "given_course_id",
            "period",
            "period_id",
            "date_absence",
            "status",
            "excluded_count",
            "comment",
            "datetime_update",
            "user",
        ]
        read_only_fields = (
            "user",
            "datetime_update",
        )


class StudentAbsenceEducSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentModel.objects.all(), source="student", required=False, allow_null=True
    )

    class Meta:
        model = StudentAbsenceEducModel
        exclude = (
            "datetime_creation",
            "datetime_update",
        )
        read_only_fields = ("user",)

        validators = [
            UniqueTogetherValidator(
                queryset=StudentAbsenceEducModel.objects.all(),
                fields=["date_absence", "period", "student"],
                message="Une absence/présence existe déjà pour cet étudiant à cette période. Actualisez la page pour mettre les données à jour.",
            )
        ]
