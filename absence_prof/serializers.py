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

from core.serializers import ResponsibleSerializer
from core.models import ResponsibleModel

from .models import Absence, MotifAbsence, AbsenceProfSettingsModel


class AbsenceProfSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceProfSettingsModel
        fields = "__all__"


class MotifAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotifAbsence
        fields = "__all__"


class AbsenceProfSerializer(serializers.ModelSerializer):
    responsible = ResponsibleSerializer(read_only=True)
    responsible_id = serializers.PrimaryKeyRelatedField(
        queryset=ResponsibleModel.objects.all(), source="matricule", required=False, allow_null=True
    )
    status = serializers.ReadOnlyField()

    def validate(self, data):
        """Ensure date_asbence_start is before date_absence_end."""

        print(data)
        if data["date_absence_start"] > data["date_absence_end"]:
            raise serializers.ValidationError(
                "La date de fin doit se trouver après la date de début."
            )
        return data

    class Meta:
        model = Absence
        exclude = ("user",)
