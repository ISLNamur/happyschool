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

from core.models import StudentModel, ResponsibleModel
from core.serializers import StudentSerializer, ResponsibleSerializer

from . import models


class FlatArrayField(fields.Field):
    def to_internal_value(self, data):
        return ";".join(data)

    def to_representation(self, value):
        return ", ".join(value.split(";"))


class PIASettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PIASettingsModel
        fields = '__all__'


class PIASerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                    source='student', required=False,
                                                    allow_null=True)

    referent = serializers.SlugRelatedField(many=True, slug_field="matricule",
                                            queryset=ResponsibleModel.objects.all())

    sponsor = serializers.SlugRelatedField(many=True, slug_field="matricule",
                                           queryset=ResponsibleModel.objects.all())

    class Meta:
        model = models.PIAModel
        fields = '__all__'


class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DisorderModel
        fields = '__all__'


class DisorderResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DisorderResponseModel
        fields = '__all__'


class CrossGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CrossGoalModel
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssessmentModel
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BranchModel
        fields = '__all__'


class BranchGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BranchGoalModel
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoalModel
        fields = '__all__'


class SubGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubGoalModel
        fields = '__all__'
