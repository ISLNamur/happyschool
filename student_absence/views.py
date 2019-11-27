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

from django.db.models import IntegerField, Sum, Case, When, Q, Subquery, F, OuterRef
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings
from django.utils import timezone

from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter

from core.utilities import get_menu, get_scholar_year
from core.people import get_classes
from core.models import ResponsibleModel, StudentModel
from core.views import BaseFilters, BaseModelViewSet

from .models import StudentAbsenceModel, StudentAbsenceSettingsModel, JustificationModel, ClasseNoteModel
from .serializers import StudentAbsenceSettingsSerializer, StudentAbsenceSerializer, JustificationSerializer, \
    ClasseNoteSerializer


def get_menu_entry(active_app: str, user) -> dict:
    if not user.has_perm('student_absence.view_studentabsencemodel'):
        return {}
    return {
            "app": "student_absence",
            "display": "Abs. Élèves",
            "url": "/student_absence",
            "active": active_app == "student_absence"
    }


def get_settings():
    settings_student_absence = StudentAbsenceSettingsModel.objects.first()
    if not settings_student_absence:
        # Create default settings.
        settings_student_absence = StudentAbsenceSettingsModel.objects.create().save()

    return settings_student_absence


class StudentAbsenceView(LoginRequiredMixin,
                         PermissionRequiredMixin,
                         TemplateView):
    template_name = "student_absence/student_absence.html"
    permission_required = ('student_absence.view_studentabsencemodel')
    filters = [
        {'value': 'student__display', 'text': 'Nom'},
        {'value': 'student__matricule', 'text': 'Matricule'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'date_absence', 'text': 'Date'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "student_absence"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceSettingsSerializer(get_settings()).data))

        return context


class StudentAbsenceFilter(BaseFilters):
    student__display = filters.CharFilter(method='people_name_by')
    classe = filters.CharFilter(method='classe_by')
    class Meta:
        fields_to_filter = ('student', 'date_absence','student__display','student__matricule',)
        model = StudentAbsenceModel
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


class StudentAbsenceViewSet(ModelViewSet):
    queryset = StudentAbsenceModel.objects.filter(student__isnull=False)
    serializer_class = StudentAbsenceSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = StudentAbsenceFilter
    ordering_fields = ('date_absence', 'datetime_update', 'datetime_creation',)

    def get_queryset(self):
        filtering = get_settings().filter_students_for_educ
        if filtering == "none" or self.request.query_params.get('forceAllAccess', False):
            return self.queryset

        classes = get_classes(check_access=True, user=self.request.user, educ_by_years=filtering == "year")
        return self.queryset.filter(student__classe__in=classes)


class AbsenceCountAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
        classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
        students = StudentModel.objects.filter(classe__in=classes)
        absences = self._filter_scholar_year(StudentAbsenceModel.objects.filter(student=OuterRef('matricule'))).values('student').annotate(
            half_days=Sum(
                Case(When(morning=True, afternoon=True, then=2), When(Q(morning=True) | Q(afternoon=True), then=1),
                     When(morning=False, afternoon=False, then=0), output_field=IntegerField()))).values('half_days')

        justif = JustificationModel.objects.filter(student=OuterRef('matricule')).values('student').annotate(
            total=Sum('half_days')).values('total')

        half_days = students.annotate(half_day_miss=Subquery(absences), half_day_just=Coalesce(Subquery(justif), 0))\
            .exclude(half_day_miss__isnull=True).annotate(half_day_diff=F('half_day_miss') - F('half_day_just'))\
            .values('matricule', 'half_day_miss', 'half_day_just', 'half_day_diff').order_by('-half_day_diff')

        # Keep only the first 15 students.
        half_days = list(map(lambda s: {**s, 'student': StudentModel.objects.get(matricule=s['matricule']).fullname_classe},
                             half_days[:15]))
        return Response(half_days)

    def _filter_scholar_year(self, queryset):
        start_year = get_scholar_year()
        end_year = start_year + 1
        start = timezone.datetime(year=start_year, month=8, day=20)
        end = timezone.datetime(year=end_year, month=8, day=19)
        return queryset.filter(datetime_creation__gt=start, datetime_creation__lt=end)


class JustificationViewSet(ReadOnlyModelViewSet):
    queryset = JustificationModel.objects.all()
    serializer_class = JustificationSerializer


class ClasseNoteViewSet(ModelViewSet):
    queryset = ClasseNoteModel.objects.all()
    serializer_class = ClasseNoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('classe',)
