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

from core.serializers import StudentSerializer, StudentModel
from . import models


class StudentAbsenceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentAbsenceSettingsModel
        fields = '__all__'


class ClasseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClasseNoteModel
        fields = '__all__'


class JustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JustificationModel
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PeriodModel
        fields = '__all__'


class StudentAbsenceSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                    source='student', required=False, allow_null=True)

    class Meta:
        model = models.StudentAbsenceModel
        exclude = ('datetime_creation', 'datetime_update',)
        read_only_fields = ('user', 'username',)

    def update(self, instance, validated_data):
        if models.StudentAbsenceSettingsModel.objects.first().sync_with_proeco:
            if not self.sync_proeco(instance, validated_data["is_absent"]):
                raise
        return super(StudentAbsenceSerializer, self).update(instance, validated_data)

    @staticmethod
    def sync_proeco(absence: models.StudentAbsenceModel, is_absent):
        from libreschoolfdb import writer

        server = [
            s['server'] for s in settings.SYNC_FDB_SERVER
            if s['teaching_name'] == absence.student.teaching.name
        ]
        if len(server) != 0:
            periods = models.PeriodModel.objects.all().order_by("start")
            period = [i for i, p in enumerate(periods) if p.id == absence.period.id][0]

            return writer.set_student_absence(
                matricule=absence.student.matricule,
                day=absence.date_absence,
                period=period,
                is_absent=is_absent,
                fdb_server=server[0]
            )
        return False
