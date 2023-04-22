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

from appels.models import Appel, MotiveModel, ObjectModel, AppelsSettingsModel
from core.serializers import (
    StudentSerializer,
    StudentModel,
    ResponsibleModel,
    ResponsibleSerializer,
)


class AppelsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppelsSettingsModel
        fields = "__all__"


class MotiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotiveModel
        fields = "__all__"


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectModel
        fields = "__all__"


class AppelSerializer(serializers.ModelSerializer):
    # In order to write with the id and read the entire object, it uses two fields field + field_id.
    matricule = StudentSerializer(read_only=True)
    matricule_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentModel.objects.all(), source="matricule", required=False, allow_null=True
    )
    responsible = ResponsibleSerializer(read_only=True)
    responsible_pk = serializers.PrimaryKeyRelatedField(
        queryset=ResponsibleModel.objects.all(),
        source="responsible",
        required=False,
        allow_null=True,
    )
    motive = MotiveSerializer(read_only=True)
    motive_id = serializers.PrimaryKeyRelatedField(
        queryset=MotiveModel.objects.all(), source="motive", write_only=True
    )
    object = ObjectSerializer(read_only=True)
    object_id = serializers.PrimaryKeyRelatedField(
        queryset=ObjectModel.objects.all(), source="object", write_only=True
    )

    class Meta:
        model = Appel
        exclude = (
            "datetime_encodage",
            "motif",
            "objet",
        )
        read_only_fields = ("user",)
