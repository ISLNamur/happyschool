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

from django_weasyprint import WeasyTemplateView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import Group

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from django_filters import rest_framework as filters

from core.utilities import get_menu
from core.views import BaseModelViewSet, get_app_settings, BaseUploadFileView, LargePageSizePagination, BaseFilters

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
    return get_app_settings(models.PIASettingsModel)


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


class PIAFilterSet(BaseFilters):
    class Meta:
        fields_to_filter = [
            "student__matricule",
            "student__last_name"
        ]
        model = models.PIAModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides


class PIAViewSet(BaseModelViewSet):
    queryset = models.PIAModel.objects.all()
    serializer_class = serializers.PIASerializer
    ordering_fields = ('student__classe__year', "student__classe__letter",)
    filter_class = PIAFilterSet

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
    pagination_class = LargePageSizePagination


class BranchGoalViewSet(ModelViewSet):
    queryset = models.BranchGoalModel.objects.all()
    serializer_class = serializers.BranchGoalSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('branch', "pia_model")
    ordering_fields = ['datetime_creation']
    ordering = ['-datetime_creation']
    pagination_class = LargePageSizePagination


class BranchStatementViewSet(ModelViewSet):
    queryset = models.BranchStatementModel.objects.all()
    serializer_class = serializers.BranchStatementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('class_council',)
    pagination_class = LargePageSizePagination


class ClassCouncilPIAViewSet(ModelViewSet):
    queryset = models.ClassCouncilPIAModel.objects.all()
    serializer_class = serializers.ClassCouncilPIASerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('pia_model',)
    ordering = ['-datetime_creation']
    pagination_class = LargePageSizePagination


class DisorderViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderModel.objects.all()
    serializer_class = serializers.DisorderSerializer
    pagination_class = LargePageSizePagination


class DisorderResponseViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderResponseModel.objects.all()
    serializer_class = serializers.DisorderResponseSerializer
    pagination_class = LargePageSizePagination


class ScheduleAdjustmentViewSet(ReadOnlyModelViewSet):
    """Read only view set for schedule adjustment model."""

    queryset = models.ScheduleAdjustmentModel.objects.all()
    serializer_class = serializers.ScheduleAdjustmentSerializer
    pagination_class = LargePageSizePagination


class CrossGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.CrossGoalItemModel.objects.all()
    serializer_class = serializers.CrossGoalItemSerializer
    pagination_class = LargePageSizePagination


class AssessmentViewSet(ReadOnlyModelViewSet):
    queryset = models.AssessmentModel.objects.all()
    serializer_class = serializers.AssessmentSerializer
    pagination_class = LargePageSizePagination


class BranchViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchModel.objects.all()
    serializer_class = serializers.BranchSerializer
    pagination_class = LargePageSizePagination


class BranchGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchGoalItemModel.objects.all()
    serializer_class = serializers.BranchGoalItemSerializer
    pagination_class = LargePageSizePagination


class UploadFileView(BaseUploadFileView):
    file_model = models.AttachmentModel
    file_serializer = serializers.AttachmentSerializer


class StudentProjectViewSet(ModelViewSet):
    queryset = models.StudentProjectModel.objects.all()
    serializer_class = serializers.StudentProjectSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('pia_model',)
    pagination_class = LargePageSizePagination
    ordering = ['-datetime_creation']


class ParentsOpinionViewSet(ModelViewSet):
    queryset = models.ParentsOpinionModel.objects.all()
    serializer_class = serializers.ParentsOpinionSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('pia_model',)
    pagination_class = LargePageSizePagination
    ordering = ['-datetime_creation']


class ReportPDFView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    WeasyTemplateView
):
    permission_required = ('pia.view_piamodel')

    template_name = "pia/report.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        try:
            context["pia"] = models.PIAModel.objects.get(id=int(kwargs["pia"]))
        except ObjectDoesNotExist:
            pass
        return context
