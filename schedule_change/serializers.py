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

from rest_framework import serializers, fields
from core.serializers import ResponsibleSerializer
from core.models import ResponsibleModel

from .models import ScheduleChangeModel, ScheduleChangeSettingsModel


class FlatArrayField(fields.Field):
    def to_internal_value(self, data):
        return ";".join(data)

    def to_representation(self, value):
        return ", ".join(value.split(";"))


class ScheduleChangeSerializer(serializers.ModelSerializer):
    send_email_general = serializers.BooleanField(write_only=True, required=False)
    send_email_substitute = serializers.BooleanField(write_only=True, required=False)
    classes = FlatArrayField()

    teachers_replaced = ResponsibleSerializer(read_only=True, many=True)
    teachers_replaced_id = serializers.SlugRelatedField(queryset=ResponsibleModel.objects.all(),
                                                        source='teachers_replaced', required=False,
                                                        allow_null=True, many=True,
                                                        slug_field='matricule')

    teachers_substitute = ResponsibleSerializer(read_only=True, many=True)
    teachers_substitute_id = serializers.SlugRelatedField(queryset=ResponsibleModel.objects.all(),
                                                          source='teachers_substitute', required=False,
                                                          allow_null=True, many=True,
                                                          slug_field='matricule')

    class Meta:
        model = ScheduleChangeModel
        fields = '__all__'
        read_only_fields = ('datetime_created', 'datetime_modified', 'user', 'created_by',)


class ScheduleChangeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangeSettingsModel
        fields = '__all__'
