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

from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.utilities import get_menu
from core.people import get_classes
from core.models import ResponsibleModel, StudentModel
from core.views import BaseFilters, BaseModelViewSet

from .models import StudentAbsenceModel, StudentAbsenceSettingsModel, JustificationModel
from .serializers import StudentAbsenceSettingsSerializer, StudentAbsenceSerializer, JustificationSerializer


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
    permission_required = ('student_absence.access_student_absence')
    filters = [{'value': 'name', 'text': 'Nom'},]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "appels"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceSettingsSerializer(get_settings()).data))

        return context


class StudentAbsenceFilter(BaseFilters):
    class Meta:
        fields_to_filter = ('student', 'date_absence',)
        model = StudentAbsenceModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides


class StudentAbsenceViewSet(BaseModelViewSet):
    queryset = StudentAbsenceModel.objects.filter(student__isnull=False)
    serializer_class = StudentAbsenceSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = StudentAbsenceFilter
    ordering_fields = ('date_absence', 'datetime_update', 'datetime_creation',)
    user_field = 'user'
    username_field = 'username'

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if get_settings().sync_with_proeco:
            self.sync_proeco(serializer.instance)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if get_settings().sync_with_proeco:
            self.sync_proeco(serializer.instance)

    @staticmethod
    def sync_proeco(obj: StudentAbsenceModel):
        from libreschoolfdb import writer

        server = [s['server'] for s in settings.SYNC_FDB_SERVER if s['teaching_name'] == obj.student.teaching.name]
        if len(server) != 0:
            writer.set_student_absence(matricule=obj.student.matricule, day=obj.date_absence,
                                       morning=obj.morning, afternoon=obj.afternoon, fdb_server=server[0])


class AbsenceCountAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
        classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
        students = StudentModel.objects.filter(classe__in=classes)
        absences = StudentAbsenceModel.objects.filter(student=OuterRef('matricule')).values('student').annotate(
            half_days=Sum(
                Case(When(morning=True, afternoon=True, then=2), When(Q(morning=True) | Q(afternoon=True), then=1),
                     When(morning=False, afternoon=False, then=0), output_field=IntegerField()))).values('half_days')

        justif = JustificationModel.objects.filter(student=OuterRef('matricule')).values('student').annotate(
            total=Sum('half_days')).values('total')

        half_days = students.annotate(half_day_miss=Subquery(absences), half_day_just=Coalesce(Subquery(justif), 0))\
            .exclude(half_day_miss__isnull=True).annotate(half_day_diff=F('half_day_miss') - F('half_day_just'))\
            .values('matricule', 'half_day_miss', 'half_day_just', 'half_day_diff').order_by('-half_day_diff')

        # Keep only the first 20 students.
        half_days = list(map(lambda s: {**s, 'student': StudentModel.objects.get(matricule=s['matricule']).fullname_classe},
                             half_days[:15]))
        return Response(half_days)


class JustificationViewSet(ReadOnlyModelViewSet):
    queryset = JustificationModel.objects.all()
    serializer_class = JustificationSerializer
