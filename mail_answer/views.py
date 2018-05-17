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

import json
import requests

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.renderers import JSONRenderer

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone

from core.models import ClasseModel

from .serializers import *
from .models import MailTemplateModel, MailAnswerModel, ChoiceModel, OptionModel, SettingsModel


permissions = (IsAuthenticated, DjangoModelPermissions,)


class OptionsViewSet(ModelViewSet):
    queryset = OptionModel.objects.all()
    serializer_class = OptionSerializer
    permission_classes = permissions


class ChoicesViewSet(ModelViewSet):
    queryset = ChoiceModel.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = permissions


class MailTemplateViewSet(ModelViewSet):
    queryset = MailTemplateModel.objects.all()
    serializer_class = MailTemplateSerializer
    permission_classes = permissions

    def get_queryset(self):
        queryset = MailTemplateModel.objects.all().order_by('datetime_creation')
        is_used = self.request.query_params.get('is_used', None)
        if is_used:
            queryset = queryset.filter(is_used=False)
        return queryset

    def perform_create(self, serializer):
        serializer.save(datetime_creation=timezone.now())


class MailAnswerViewSet(ModelViewSet):
    queryset = MailAnswerModel.objects.all()
    serializer_class = MailAnswerSerializer
    permission_classes = permissions


class MailAnswerUpdateViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    """
    Access and update for anybody that has the uuid (no auth required).
    """
    queryset = MailAnswerModel.objects.all()
    serializer_class = MailAnswerSerializer

    def perform_update(self, serializer):
        serializer.save(is_answered=True)


class MailAnswerView(LoginRequiredMixin,
                     PermissionRequiredMixin,
                     TemplateView):
    template_name = "mail_answer/mail_answer.html"
    permission_required = ('mail_answer.add_mailanswermodel')

    def get_context_data(self, **kwargs):
        # Get settings.
        settings = SettingsModel.objects.first()
        if not settings:
            # Create default settings.
            SettingsModel.objects.create().save()
        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context['settings'] = JSONRenderer().render(SettingsSerializer(settings).data).decode()
        return context


class AnswerView(TemplateView):
    template_name = "mail_answer/answer.html"


class Answer(object):
    def __init__(self, classe, student_name, answer, is_answered):
        self.classe = classe
        self.student_name = student_name
        self.answer = answer
        self.is_answered = is_answered


class AnswerClasse(object):
    def __init__(self, classe_id, classe_name, classe_year, answered_count, answers_count):
        self.classe_id = classe_id
        self.classe_name = classe_name
        self.classe_year = classe_year
        self.answered_count = answered_count
        self.answers_count = answers_count


class AnswersClassesAPI(APIView):
    queryset = MailAnswerModel.objects.all()
    serializer_class = MailAnswerSerializer
    permission_classes = permissions

    def get(self, request, *args, **kwargs):
        template_id = kwargs.get('template', -1)
        answers = MailAnswerModel.objects.filter(template__id=template_id)
        classes_id = answers.distinct('student__classe').values_list('student__classe', flat=True)
        answers_classes = []
        for c in classes_id:
            classe = ClasseModel.objects.get(id=c)
            name = str(classe)
            year = classe.year
            answers_count = answers.filter(student__classe__id=c).count()
            answered_count = answers.filter(student__classe__id=c, is_answered=True).count()
            # Create the object to serialize.
            answers_classes.append(AnswerClasse(classe_id=c, classe_name=name, classe_year=year,
                                                answered_count=answered_count,
                                                answers_count=answers_count))
        serializer = AnswerClasseSerializer(sorted(answers_classes, key=lambda c: c.classe_name), many=True)
        return Response(serializer.data)


class AnswersAPI(APIView):
    queryset = MailAnswerModel.objects.all()
    serializer_class = MailAnswerSerializer
    permission_classes = permissions

    def get(self, request, *args, **kwargs):
        template_id = kwargs.get('template', -1)
        classe_id = kwargs.get('classe', -1)
        queryset = MailAnswerModel.objects.filter(template__id=template_id,
                                                  student__classe__id=classe_id)
        answers = map(self.answer_model_to_object, queryset)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    @staticmethod
    def answer_model_to_object(model):
        classe = str(model.student.classe)
        name = model.student.fullname
        is_answered= len(model.answers) > 2
        answer = model.answers
        return Answer(classe=classe, student_name=name, is_answered=is_answered, answer=answer)
