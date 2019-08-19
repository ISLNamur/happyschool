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

from core.serializers import StudentSerializer
from core.models import StudentModel

from .models import StudentAbsenceTeacherSettingsModel, StudentAbsenceTeacherModel, StudentLatenessTeacherModel, PeriodModel, LessonModel


class StudentAbsenceTeacherSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAbsenceTeacherSettingsModel
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodModel
        fields = ('id', 'name', 'start', 'end', 'display',)

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'


class StudentAbsenceTeacherSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields: field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                    source='student', required=False, allow_null=True)
    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=LessonModel.objects.all(),
                                                   source='lesson', required=False, allow_null=True)

    period = PeriodSerializer(read_only=True)
    period_id = serializers.PrimaryKeyRelatedField(queryset=PeriodModel.objects.all(),
                                                   source='period', required=False, allow_null=True)

    class Meta:
        model = StudentAbsenceTeacherModel
        exclude = ('datetime_creation', 'datetime_update',)
        read_only_fields = ('user',)


class StudentLatenessTeacherSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields: field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                    source='student', required=False, allow_null=True)

    lesson = LessonSerializer(read_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=LessonModel.objects.all(),
                                                   source='lesson', required=False, allow_null=True)

    period = PeriodSerializer(read_only=True)
    period_id = serializers.PrimaryKeyRelatedField(queryset=PeriodModel.objects.all(),
                                                   source='period', required=False, allow_null=True)

    class Meta:
        model = StudentLatenessTeacherModel
        exclude = ('datetime_creation', 'datetime_update',)
        read_only_fields = ('user',)
