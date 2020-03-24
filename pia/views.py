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
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from django_filters import rest_framework as filters

from core.models import TeachingModel
from core.utilities import get_menu
from core.views import BaseModelViewSet

from . import models
from . import serializers


def get_menu_entry(active_app: str, user) -> dict:
    if not user.has_perm('pia.view_piamodel'):
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
    permission_required = ('pia.view_piamodel',)
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
        context['can_add_pia'] = json.dumps(self.request.user.has_perm('pia.add_piamodel'))

        return context


class LargePagination(PageNumberPagination):
    """A default pagination of 500 items."""
    page_size = 500


class PIAViewSet(BaseModelViewSet):
    queryset = models.PIAModel.objects.all()
    serializer_class = serializers.PIASerializer
    ordering_fields = ('student__classe__year', "student__classe__letter",)
    filterset_fields = ('student__matricule',)

    username_field = None

    def is_only_tenure(self):
        return get_settings().filter_teacher_entries_by_tenure


class CrossGoalViewSet(ModelViewSet):
    queryset = models.CrossGoalModel.objects.all()
    serializer_class = serializers.CrossGoalSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('pia_model',)
    ordering_fields = ['date_start', 'date_end', 'datetime_creation']
    ordering = ['-date_start']
    pagination_class = LargePagination


class BranchGoalViewSet(ModelViewSet):
    queryset = models.BranchGoalModel.objects.all()
    serializer_class = serializers.BranchGoalSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('branch',)
    ordering_fields = ['datetime_creation']
    ordering = ['-datetime_creation']
    pagination_class = LargePagination


class BranchStatementViewSet(ModelViewSet):
    queryset = models.BranchStatementModel.objects.all()
    serializer_class = serializers.BranchStatementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('class_council',)
    pagination_class = LargePagination


class ClassCouncilPIAViewSet(ModelViewSet):
    queryset = models.ClassCouncilPIAModel.objects.all()
    serializer_class = serializers.ClassCouncilPIASerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('pia_model',)
    pagination_class = LargePagination


class DisorderViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderModel.objects.all()
    serializer_class = serializers.DisorderSerializer
    pagination_class = LargePagination


class DisorderResponseViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderResponseModel.objects.all()
    serializer_class = serializers.DisorderResponseSerializer
    pagination_class = LargePagination


class ScheduleAdjustmentViewSet(ReadOnlyModelViewSet):
    """Read only view set for schedule adjustment model."""

    queryset = models.ScheduleAdjustmentModel.objects.all()
    serializer_class = serializers.ScheduleAdjustmentSerializer
    pagination_class = LargePagination


class CrossGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.CrossGoalItemModel.objects.all()
    serializer_class = serializers.CrossGoalItemSerializer
    pagination_class = LargePagination


class AssessmentViewSet(ReadOnlyModelViewSet):
    queryset = models.AssessmentModel.objects.all()
    serializer_class = serializers.AssessmentSerializer
    pagination_class = LargePagination


class BranchViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchModel.objects.all()
    serializer_class = serializers.BranchSerializer
    pagination_class = LargePagination


class BranchGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchGoalItemModel.objects.all()
    serializer_class = serializers.BranchGoalItemSerializer
    pagination_class = LargePagination
