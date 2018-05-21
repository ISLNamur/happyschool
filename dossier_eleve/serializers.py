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

from core.serializers import StudentSerializer
from .models import *


class DossierEleveSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierEleveSettingsModel
        fields = '__all__'


class InfoEleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoEleve
        fields = '__all__'


class SanctionDecisionDisciplinaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanctionDecisionDisciplinaire
        fields = '__all__'


class CasEleveSerializer(serializers.ModelSerializer):
    send_to_teachers = serializers.BooleanField(write_only=True, required=False)

    matricule = StudentSerializer(read_only=True)
    matricule_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                      source='matricule', required=False,
                                                      allow_null=True)
    info = InfoEleveSerializer(read_only=True)
    info_id = serializers.PrimaryKeyRelatedField(queryset=InfoEleve.objects.all(),
                                                      source='info', required=False,
                                                      allow_null=True)

    sanction_decision = SanctionDecisionDisciplinaireSerializer(read_only=True)
    sanction_decision_id = serializers.PrimaryKeyRelatedField(queryset=SanctionDecisionDisciplinaire.objects.all(),
                                                 source='sanction_decision', required=False,
                                                 allow_null=True)

    class Meta:
        model = CasEleve
        fields = '__all__'
        read_only_fields = ('user', 'datetime_encodage',)
