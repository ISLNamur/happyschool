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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter

from core.utilities import get_menu, get_scholar_year
from core.people import get_classes
from core.models import ResponsibleModel, StudentModel
from core.views import BaseFilters, PageNumberSizePagination, get_app_settings

from .models import StudentAbsenceModel, StudentAbsenceSettingsModel, JustificationModel, ClasseNoteModel,\
    PeriodModel
from .serializers import StudentAbsenceSettingsSerializer, StudentAbsenceSerializer, JustificationSerializer,\
    ClasseNoteSerializer, PeriodSerializer


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
    return get_app_settings(StudentAbsenceSettingsModel)


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
        {'value': 'activate_is_absent', 'text': 'Absences uniquement'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "student_absence"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceSettingsSerializer(get_settings()).data))
        context["proeco"] = json.dumps("proeco" in settings.INSTALLED_APPS)

        return context


class StudentAbsenceFilter(BaseFilters):
    student__display = filters.CharFilter(method='people_name_by')
    classe = filters.CharFilter(method='classe_by')
    activate_is_absent = filters.BooleanFilter(method="activate_is_absent_by")

    class Meta:
        fields_to_filter = ('student', 'date_absence',
            'student__matricule', 'is_absent',)
        model = StudentAbsenceModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_is_absent_by(self, queryset, name, value):
        return queryset.filter(is_absent=True)


class StudentAbsenceViewSet(ModelViewSet):
    queryset = StudentAbsenceModel.objects.filter(student__isnull=False)
    serializer_class = StudentAbsenceSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = StudentAbsenceFilter
    pagination_class = PageNumberSizePagination
    ordering_fields = ('date_absence', 'datetime_update', 'datetime_creation',)
    cursor = None

    def get_queryset(self):
        filtering = get_settings().filter_students_for_educ
        force_all_access = self.request.query_params.get('forceAllAccess', "false")
        force_all_access = json.loads(force_all_access) if force_all_access else False
        if filtering == "none" or force_all_access:
            return self.queryset

        classes = get_classes(check_access=True, user=self.request.user, educ_by_years=filtering == "year")
        return self.queryset.filter(student__classe__in=classes)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list) and len(request.data) == 0:
            return Response(status=status.HTTP_201_CREATED)

        if get_settings().sync_with_proeco:
            from libreschoolfdb import absences

            teaching = request.data[0].get('student')["teaching"]["name"] if isinstance(request.data, list) else request.data.get("student")["teaching"]["name"]
            server = [
                s['server'] for s in settings.SYNC_FDB_SERVER
                if s['teaching_name'] == teaching
            ]
            if len(server) == 0:
                raise
            self.cursor = absences._get_absence_cursor(fdb_server=server[0])

        # if isinstance(request.data, list) and len(request.data) > 0:
        absences_done = []
        for absence in request.data:
            serializer = self.get_serializer(data=absence)
            serializer.is_valid(raise_exception=True)
            if get_settings().sync_with_proeco:
                if not self.sync_proeco(serializer.validated_data):
                    continue
            self.perform_create(serializer)
            absences_done.append(serializer.data)
        if get_settings().sync_with_proeco:
            self.cursor.connection.commit()
            self.cursor.connection.close()
        return Response(absences_done, status=status.HTTP_201_CREATED)

    def sync_proeco(self, data: dict):
        from libreschoolfdb import writer

        if self.cursor:
            periods = PeriodModel.objects.all().order_by("start")
            period = [i for i, p in enumerate(periods) if p.id == data.get("period", None).id][0]

            return writer.set_student_absence(
                matricule=data.get('student').matricule,
                day=data.get('date_absence'),
                period=period,
                is_absent=data.get("is_absent", False),
                cur=self.cursor,
                commit=False
            )
        return False


if "proeco" in settings.INSTALLED_APPS:
    from proeco.views import ExportStudentSelectionAPI

    class ExportStudentAbsenceAPI(ExportStudentSelectionAPI):
        """Export in a file the current list view as a proeco selection."""
        def _get_student_list(self, request):
            view_set = StudentAbsenceViewSet.as_view({'get': 'list'})
            absences = [a["student_id"] for a in view_set(request._request).data['results']]
            return absences


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


class PeriodViewSet(ReadOnlyModelViewSet):
    queryset = PeriodModel.objects.all()
    serializer_class = PeriodSerializer
