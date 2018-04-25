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

from rest_framework import serializers

from appels.models import Appel, MotiveModel, ObjectModel


class AppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appel
        exclude = ('datetime_encodage',)
        read_only_fields = ('user', 'name',)


class MotiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotiveModel
        fields = '__all__'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectModel
        fields = '__all__'
