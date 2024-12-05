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

    def update(self, instance, validated_data):
        if (
            StudentAbsenceTeacherSettingsModel.objects.first().sync_with_proeco
            and "status" in validated_data
        ):
            if not self.sync_proeco(instance, validated_data["status"]):
                raise
        return super(StudentAbsenceEducSerializer, self).update(instance, validated_data)

    @staticmethod
    def sync_proeco(absence: StudentAbsenceEducModel, absence_status):
        from libreschoolfdb import writer

        server = [
            s["server"]
            for s in settings.SYNC_FDB_SERVER
            if s["teaching_name"] == absence.student.teaching.name
        ]
        if len(server) != 0:
            periods = PeriodEducModel.objects.all().order_by("start")
            period = [i for i, p in enumerate(periods) if p.id == absence.period.id][0]

            return writer.set_student_absence(
                matricule=absence.student.matricule,
                day=absence.date_absence,
                period=period,
                absence_status=absence_status,
                fdb_server=server[0],
            )[0]
        return False
