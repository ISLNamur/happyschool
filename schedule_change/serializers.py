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

from .models import ScheduleChangeModel, ScheduleChangeSettingsModel, ScheduleChangeTypeModel, ScheduleChangePlaceModel,\
    ScheduleChangeCategoryModel


class FlatArrayField(fields.Field):
    def to_internal_value(self, data):
        return ";".join(data)

    def to_representation(self, value):
        return ", ".join(value.split(";"))


class ScheduleChangeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangeTypeModel
        fields = '__all__'


class ScheduleChangeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangeCategoryModel
        fields = '__all__'

class ScheduleChangePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangePlaceModel
        fields = '__all__'


class ScheduleChangeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=False, required=False)
    send_email_general = serializers.BooleanField(write_only=True, required=False)
    send_email_substitute = serializers.BooleanField(write_only=True, required=False)
    send_email_replaced = serializers.BooleanField(write_only=True, required=False)
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
        fields = [
            "id", "change", "category", "date_change", "time_start", "time_end",
            "send_email_general", "send_email_substitute", "teachers_replaced",
            "teachers_replaced_id", "teachers_substitute", "teachers_substitute_id",
            "classes", "place", "comment", "hide_for_students", "send_email_replaced"
            ]
        read_only_fields = ('datetime_created', 'datetime_modified', 'user', 'created_by',)


class ScheduleChangeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleChangeSettingsModel
        fields = '__all__'
