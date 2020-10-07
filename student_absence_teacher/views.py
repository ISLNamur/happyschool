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
import datetime
from itertools import groupby

from django.db.models import Count
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter

from core.models import ClasseModel
from core.utilities import get_menu
from core.views import BaseFilters, PageNumberSizePagination

from .models import StudentAbsenceTeacherSettingsModel, StudentAbsenceTeacherModel, PeriodModel, LessonModel
from .serializers import StudentAbsenceTeacherSettingsSerializer, PeriodSerializer, StudentAbsenceTeacherSerializer


def get_menu_entry(active_app: str, user) -> dict:
    if not user.has_perm('student_absence_teacher.view_studentabsenceteachermodel'):
        return {}
    return {
            "app": "student_absence_teacher",
            "display": "Abs. Élèves (prof)",
            "url": "/student_absence_teacher",
            "active": active_app == "student_absence_teacher"
    }


def get_settings():
    settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.first()
    if not settings_student_absence:
        # Create default settings.
        settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.create().save()

    return settings_student_absence


class StudentAbsenceTeacherView(LoginRequiredMixin,
                                PermissionRequiredMixin,
                                TemplateView):
    template_name = "student_absence_teacher/student_absence_teacher.html"
    permission_required = ('student_absence_teacher.view_studentabsenceteachermodel')
    filters = [
        {'value': 'student__display', 'text': 'Nom'},
        {'value': 'student__matricule', 'text': 'Matricule'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'date_absence', 'text': 'Date absence'},
        {'value': 'date_lateness', 'text': 'Date retard'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "student_absence_absence"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceTeacherSettingsSerializer(get_settings()).data))

        return context


class StudentAbsenceTeacherFilter(BaseFilters):
    student__display = filters.CharFilter(method='people_name_by')
    classe = filters.CharFilter(method='classe_by')

    class Meta:
        fields_to_filter = ['student', 'date_absence', 'student__matricule', 'student__classe', "period"]
        model = StudentAbsenceTeacherModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, field_name, value):
        if not value[0].isdigit():
            return queryset

        if len(value) > 0:
            queryset = queryset.filter(student__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(student__classe__letter__istartswith=value[1:])
        return queryset


class StudentAbsenceTeacherViewSet(ModelViewSet):
    queryset = StudentAbsenceTeacherModel.objects.filter(student__isnull=False)
    serializer_class = StudentAbsenceTeacherSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = StudentAbsenceTeacherFilter
    ordering_fields = ['date_absence', 'datetime_update', 'datetime_creation', 'period']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PeriodViewSet(ReadOnlyModelViewSet):
    queryset = PeriodModel.objects.all().order_by("start")
    serializer_class = PeriodSerializer


class OverviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def _merge_count(self, classe_id, row, periods):
        counts = {
            "classe": ClasseModel.objects.get(id=classe_id).compact_str,
            "classe__id": classe_id
        }
        for period in periods:
            counts["period-" + str(period)] = next(
                (x["id__count"] for x in row \
                    if x["period"] == period and x["status"] == StudentAbsenceTeacherModel.ABSENCE),
                next((0 for y in row if y["period"] == period), -1)
            )
        return counts

    def get(self, request, date, format=None):
        date = datetime.date.fromisoformat(date)
        periods = PeriodModel.objects.values_list("id", flat=True)
        raw_count = StudentAbsenceTeacherModel.objects \
            .exclude(status=StudentAbsenceTeacherModel.LATENESS) \
            .filter(date_absence=date) \
            .order_by("student__classe__id") \
            .values("student__classe__id", "period", "status").annotate(Count("id"))

        count_by_classe_by_period = [
            self._merge_count(k, list(row), periods)
            for k, row in groupby(raw_count, key=lambda c: c["student__classe__id"])
        ]

        return Response(json.dumps(count_by_classe_by_period))
