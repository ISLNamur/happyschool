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

from .models import ChoiceModel, OptionModel, MailTemplateModel, MailAnswerModel


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
        fields = '__all__'

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        options = validated_data.pop('options')

        mail_template = MailTemplateModel.objects.create(**validated_data)
        for choice in choices:
            choice_model = ChoiceModel.objects.create(**choice)
            mail_template.choices.append(choice_model)
        for option in options:
            option_model = OptionModel.objects.create(**option)
            mail_template.options.append(option_model)

        return mail_template


class MailAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailAnswerModel
        fields = '__all__'
