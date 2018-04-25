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

from core.models import ResponsibleModel, StudentModel


class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'last_name', 'first_name', 'is_secretary', 'email', 'email_alias', 'teaching')
        depth = 1


class ResponsibleSensitiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsibleModel
        fields = ('pk', 'last_name', 'first_name', 'is_secretary', 'email_alias', 'teaching')
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModel
        fields = '__all__'
        depth = 1
