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
from core.people import check_access_to_student

from .models import *
from . import views


class DossierEleveSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierEleveSettingsModel
        fields = "__all__"


class InfoEleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoEleve
        fields = "__all__"


class SanctionDecisionDisciplinaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanctionDecisionDisciplinaire
        fields = "__all__"


class CasEleveSerializer(serializers.ModelSerializer):
    send_to_teachers = serializers.BooleanField(write_only=True, required=False)

    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=StudentModel.objects.all(), source="student", required=False, allow_null=True
    )
    info = InfoEleveSerializer(read_only=True)
    info_id = serializers.PrimaryKeyRelatedField(
        queryset=InfoEleve.objects.all(), source="info", required=False, allow_null=True
    )

    sanction_decision = SanctionDecisionDisciplinaireSerializer(read_only=True)
    sanction_decision_id = serializers.PrimaryKeyRelatedField(
        queryset=SanctionDecisionDisciplinaire.objects.all(),
        source="sanction_decision",
        required=False,
        allow_null=True,
    )

    def validate_sanction_decision_id(self, value):
        # If submit sanction is not enable, ignore validation.
        if not views.get_settings().enable_submit_sanctions:
            return value
        if value and not self.context["request"].user.has_perm("dossier_eleve.ask_sanction"):
            raise serializers.ValidationError(
                "Vous n'avez pas les droits nécessaire pour ajouter/modifier une sanction"
            )
        return value

    def validate_date_sanction(self, value):
        if not self.context["request"].user.has_perm("dossier_eleve.set_sanction") and value:
            raise serializers.ValidationError(
                "Vous n'avez pas les droits nécessaire pour ajouter/modifier la date d'une sanction"
            )
        return value

    def validate_sanction_faite(self, value):
        if not self.context["request"].user.has_perm("dossier_eleve.set_sanction") and value:
            raise serializers.ValidationError(
                "Vous n'avez pas les droits nécessaire pour mettre une sanction comme faite"
            )
        return value

    def validate_student_id(self, value):
        # Only dossier_eleve need to be checked.
        if self.context["request"].path.startswith("/dossier_eleve/api/ask_sanctions/"):
            return value

        if not check_access_to_student(
            value, self.context["request"].user, tenure_class_only=False
        ):
            raise serializers.ValidationError(
                "Vous n'avez pas les droits nécessaire pour ajouter cet élève"
            )
        return value

    class Meta:
        model = CasEleve
        fields = "__all__"
        read_only_fields = (
            "user",
            "datetime_encodage",
        )


class CasAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CasAttachment
        fields = "__all__"
