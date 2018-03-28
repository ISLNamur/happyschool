# This file is part of Appyschool.
#
# Appyschool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# Appyschool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Appyschool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers, fields
from .models import ScheduleChange, ScheduleChangeSettings


class FlatArrayField(fields.Field):
    def to_internal_value(self, data):
        return ";".join(data)

    def to_representation(self, value):
        return ", ".join(value.split(";"))


class ScheduleChangeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField()
    datetime_encodage = serializers.ReadOnlyField()
    classes = FlatArrayField()
    teachers = FlatArrayField()
    time_start = serializers.TimeField(allow_null=True)
    time_end = serializers.TimeField(allow_null=True)

    class Meta:
        model = ScheduleChange
        fields = ('id', 'date_start', 'date_end', 'time_start',
                  'time_end', 'activity', 'classes', 'teachers', 'place', 'comment', 'user', 'datetime_encodage')


class ScheduleChangeSettingsSerializer(serializers.ModelSerializer):
    teaching = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = ScheduleChangeSettings
        fields = '__all__'
