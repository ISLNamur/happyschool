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

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.models import TeachingModel
from core.utilities import get_menu
from core.views import BaseModelViewSet

from . import models
from . import serializers


def get_menu_entry(active_app: str, user) -> dict:
    if not user.has_perm('pia.view_pia'):
        return {}
    return {
            "app": "pia",
            "display": "PIA",
            "url": "/pia",
            "active": active_app == "pia"
    }


def get_settings():
    settings_pia = models.PIASettingsModel.objects.first()
    if not settings_pia:
        # Create default settings.
        settings_pia = models.PIASettingsModel.objects.create()
        # If only one teaching exist, assign it.
        if TeachingModel.objects.count() == 1:
            settings_pia.teachings.add(TeachingModel.objects.first())
        settings_pia.save()

    return settings_pia


class PIAView(LoginRequiredMixin,
              PermissionRequiredMixin,
              TemplateView):
    template_name = "pia/pia.html"
    permission_required = ('pia.view_pia')
    filters = [
        {'value': 'student__display', 'text': 'Nom'},
        {'value': 'student__matricule', 'text': 'Matricule'},
        {'value': 'classe', 'text': 'Classe'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "pia"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((serializers.PIASettingsSerializer(get_settings()).data))

        return context


class PIAViewSet(BaseModelViewSet):
    queryset = models.PIAModel.objects.filter(student__inactive_from__isnull=True)
    serializer_class = serializers.PIASerializer
    username_field = None


class DisorderViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderModel.objects.all()
    serializer_class = serializers.DisorderSerializer


class DisorderResponseViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderResponseModel.objects.all()
    serializer_class = serializers.DisorderResponseSerializer


class CrossGoalViewSet(ReadOnlyModelViewSet):
    queryset = models.CrossGoalModel.objects.all()
    serializer_class = serializers.CrossGoalSerializer


class AssessmentViewSet(ReadOnlyModelViewSet):
    queryset = models.AssessmentModel.objects.all()
    serializer_class = serializers.AssessmentSerializer


class BranchViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchModel.objects.all()
    serializer_class = serializers.BranchSerializer


class BranchGoalViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchGoalModel.objects.all()
    serializer_class = serializers.BranchGoalSerializer
