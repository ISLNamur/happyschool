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
from .models import StudentAbsenceSettingsModel, StudentAbsenceModel, JustificationModel


class StudentAbsenceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAbsenceSettingsModel
        fields = '__all__'


class JustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JustificationModel
        fields = '__all__'


class StudentAbsenceSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields field + field_id.
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                   source='student', required=False, allow_null=True)

    class Meta:
        model = StudentAbsenceModel
        exclude = ('datetime_creation', 'datetime_update',)
        read_only_fields = ('user', 'username',)

    def create(self, validated_data):
        if StudentAbsenceSettingsModel.objects.first().sync_with_proeco:
            self.sync_proeco(validated_data)
        return super(StudentAbsenceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if StudentAbsenceSettingsModel.objects.first().sync_with_proeco:
            self.sync_proeco(validated_data)
        return super(StudentAbsenceSerializer, self).update(instance, validated_data)

    @staticmethod
    def sync_proeco(data: dict):
        from libreschoolfdb import writer

        server = [s['server'] for s in settings.SYNC_FDB_SERVER if s['teaching_name'] == data.get('student').teaching.name]
        if len(server) != 0:
            writer.set_student_absence(matricule=data.get('student').matricule, day=data.get('date_absence'),
                                       morning=data.get('morning', None), afternoon=data.get('afternoon', None),
                                       fdb_server=server[0])
