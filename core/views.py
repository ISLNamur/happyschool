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
import warnings
import requests

from datetime import date, timedelta

from icalendar import Calendar

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import CharField, Q
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.views.generic import TemplateView
from django.contrib.auth.models import Group

from core.models import ResponsibleModel, TeachingModel, EmailModel, CoreSettingsModel, StudentModel,\
    ImportCalendarModel, ClasseModel
from core.people import get_classes
from core.permissions import IsSecretaryPermission
from core.serializers import ResponsibleSensitiveSerializer, TeachingSerializer,\
    EmailSerializer, ClasseSerializer, ResponsibleRemoteSerializer, StudentWriteSerializer
from core.utilities import get_scholar_year, get_menu


def get_core_settings():
    settings_core = CoreSettingsModel.objects.first()
    if not settings_core:
        # Create default settings.
        settings_core = CoreSettingsModel.objects.create().save()

    return settings_core


class BaseFilters(filters.FilterSet):
    datetime_field = "datetime_encodage"

    unique = filters.CharFilter('unique_by', method='unique_by')
    scholar_year = filters.CharFilter(method='scholar_year_by')

    class Meta:
        fields_to_filter = set()

        def generate_filters(fields) -> dict:
            filters = {}
            for f in fields:
                is_date_or_time = f.startswith("date") or f.startswith("time")
                filters[f] = ['exact'] if not is_date_or_time else ['lt', 'gt', 'lte', 'gte', 'exact']
            return filters
        fields = generate_filters(fields_to_filter)
        filter_overrides = {
            CharField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'unaccent__icontains',
                },
            },
        }

    def unique_by(self, queryset, field_name, value):
        if value:
            # Distinct query in postgrsql asks to order_by the same column.
            return queryset.order_by(value).distinct(value)
        else:
            return queryset

    def scholar_year_by(self, queryset, field_name, value):
        start_year = int(value[:4])
        end_year = start_year + 1
        start = timezone.datetime(year=start_year, month=8, day=20)
        end = timezone.datetime(year=end_year, month=8, day=19)
        return queryset.filter(**{self.datetime_field + "__gt": start, self.datetime_field + "__lt": end})
    
    def people_name_by(self, queryset, name, value):
        tokens = value.split(" ")
        people = queryset.none()

        if len(tokens) > 1:
            # First check compound last name.
            people = queryset.filter(Q(student__last_name__unaccent__istartswith=" ".join(tokens[:2]))
                                     | Q(student__last_name__unaccent__istartswith=" ".join(tokens[-2:])))
            if len(people) == 0:
                people = queryset.filter(Q(student__first_name__unaccent__iexact=tokens[0],
                                           student__last_name__unaccent__istartswith=tokens[1])
                                         | Q(student__first_name__unaccent__istartswith=tokens[1],
                                             student__last_name__unaccent__iexact=tokens[0]))

        if len(people) == 0:
            for name_part in tokens:
                people |= queryset.filter(Q(student__first_name__unaccent__istartswith=name_part)
                                                    | Q(student__last_name__unaccent__istartswith=name_part))
        return people


class PageNumberSizePagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 1000


class BaseModelViewSet(ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    permission_classes = (DjangoModelPermissions,)
    pagination_class = PageNumberSizePagination
    user_field = None
    username_field = "user"

    def get_queryset(self):
        if self.request.user.groups.intersection(self.get_group_all_access()).exists():
            return self.queryset
        else:
            try:
                teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
                classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user,
                                      tenure_class_only=self.is_only_tenure())
                try:
                    queryset = self.queryset.filter(student__classe__in=classes)
                except FieldError:
                    queryset = self.queryset.filter(matricule__classe__in=classes)
                    warnings.warn("Use *student* as field name instead of matricule", DeprecationWarning)
                return queryset
            except ObjectDoesNotExist:
                return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save()
        if self.username_field:
            serializer.save(**{
                self.username_field: self.request.user.username,
                }
            )
        if self.user_field:
            serializer.save(**{
                self.user_field: self.request.user,
            })

    def get_group_all_access(self):
        return Group.objects.none()

    def is_only_tenure(self):
        return True


class MembersView(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  TemplateView):
    template_name = "core/members.html"
    permission_required = ('core.add_responsiblemodel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = json.dumps(get_menu(self.request.user))
        return context


class ProfilView(LoginRequiredMixin, TemplateView):
    template_name = 'core/profil.html'


class MembersAPI(ModelViewSet):
    queryset = ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)
    serializer_class = ResponsibleSensitiveSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)

    def get_queryset(self):
        person_type = self.request.GET.get('person_type', None)
        if person_type == 'secretary':
            return ResponsibleModel.objects.filter(is_secretary=True)
        elif person_type == 'others':
            return ResponsibleModel.objects.filter(is_teacher=False, is_educator=False, is_secretary=False)
        else:
            return ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)


class ScholarYearAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        query = self.request.GET.get('scholar_year', '')
        if not query:
            return Response([])

        current_year = get_scholar_year()
        options = []
        for y in reversed(range(current_year - 10, current_year + 1)):
            options.append("%i-%i" % (y, y + 1))
        return Response(options)


class TeachingViewSet(ModelViewSet):
    queryset = TeachingModel.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions)


class ClasseViewSet(ModelViewSet):
    queryset = ClasseModel.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class ResponsibleViewSet(ModelViewSet):
    queryset = ResponsibleModel.objects.all()
    serializer_class = ResponsibleRemoteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class StudentViewSet(ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentWriteSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class EmailViewSet(ReadOnlyModelViewSet):
    queryset = EmailModel.objects.all().order_by("display")
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)


class BirthdayAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        people = self.request.GET.get('people', 'student')

        birthday = []
        today = timezone.now()
        if people == 'student':
            students = StudentModel.objects.filter(additionalstudentinfo__birth_date__month=today.month,
                                                   additionalstudentinfo__birth_date__day=today.day,
                                                   classe__isnull=False).order_by('teaching')
            students = students.values_list('last_name', 'first_name', 'classe__year', 'classe__letter')
            birthday += [{'name': "%s %s %s%s" % (s[0], s[1], s[2], s[3].upper())} for s in students]
        return Response({'results': birthday})


class CalendarAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _today(event):
        now = timezone.now()
        if type(event['DTSTART'].dt) == date:
            return now.date()
        return now

    @staticmethod
    def _format_date(date, is_end=False):
        if ":" in str(date):
            print(date.strftime("%H:%M" if is_end else "%d/%m/%Y %H:%M"))
            return date.strftime("%H:%M" if is_end else "%d/%m/%Y %H:%M")
        else:
            if is_end:
                return (date - timedelta(days=1)).strftime("%d/%m/%Y")
            else:
                return date.strftime("%d/%m/%Y")

    # Cache for 6 hours.
    @method_decorator(cache_page(60 * 60 * 6))
    def get(self, format=None):
        events = []
        for cal_ics in ImportCalendarModel.objects.all():
            cal = Calendar.from_ical(requests.get(cal_ics.url).text)
            #for e in cal.walk('VEVENT'):
            #    if e['DTSTART'].dt > self._today(e) or e['DTSTART'].dt <= self._today(e) < e['DTEND'].dt:
            #        print(e['DTEND'].dt)
            evts = [{"calendar": cal_ics.name,"name": str(event['SUMMARY']), "begin": self._format_date(event['DTSTART'].dt),
                     "end": self._format_date(event['DTEND'].dt, True)} for event in cal.walk('VEVENT')
                    if event['DTSTART'].dt > self._today(event) or event['DTSTART'].dt <= self._today(event) < event['DTEND'].dt]
            events += evts
        events = sorted(events, key=lambda e: (e["begin"][6:], e["begin"][3:5], e["begin"][:2]))
        return Response({'results': events})


class PingAPI(APIView):
    def get(self, format=None):
        return Response(status=HTTP_200_OK, data={})
