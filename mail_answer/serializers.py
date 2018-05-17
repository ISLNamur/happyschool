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

from .models import ChoiceModel, OptionModel, MailTemplateModel, MailAnswerModel, SettingsModel


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceModel
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionModel
        fields = '__all__'


class MailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailTemplateModel
        exclude = ('datetime_creation',)


class MailAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailAnswerModel
        fields = '__all__'
        read_only_fields = ('uuid', 'student', 'template')

        depth = 2


class AnswerSerializer(serializers.Serializer):
    classe = serializers.CharField(max_length=200)
    student_name = serializers.CharField(max_length=100)
    answer = serializers.JSONField()
    is_answered = serializers.BooleanField()


class AnswerClasseSerializer(serializers.Serializer):
    classe_id = serializers.IntegerField()
    classe_name = serializers.CharField(max_length=200)
    classe_year = serializers.IntegerField()
    answered_count = serializers.IntegerField()
    answers_count = serializers.IntegerField()
