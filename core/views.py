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

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from django.utils import timezone
from django.db.models import CharField
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.views.generic import TemplateView
from django.contrib.auth.models import Group

from core.models import ResponsibleModel, TeachingModel, EmailModel
from core.people import get_classes
from core.permissions import IsSecretaryPermission
from core.serializers import ResponsibleSensitiveSerializer, TeachingSerializer,\
    EmailSerializer
from core.utilities import get_scholar_year, get_menu


class BaseFilters(filters.FilterSet):
    unique = filters.CharFilter('unique_by', method='unique_by')
    scholar_year = filters.CharFilter(method='scholar_year_by')

    class Meta:
        fields_to_filter = set()

        def generate_filters(fields) -> dict:
            filters = {}
            for f in fields:
                is_date_or_time = f.startswith("date") or f.startswith("time")
                filters[f] = ['exact'] if not is_date_or_time else ['lt', 'gt']
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

    def unique_by(self, queryset, name, value):
        if value:
            # Distinct query in postgrsql asks to order_by the same column.
            return queryset.order_by(value).distinct(value)
        else:
            return queryset

    def scholar_year_by(self, queryset, name, value):
        start_year = int(value[:4])
        end_year = start_year + 1
        start = timezone.datetime(year=start_year, month=8, day=20)
        end = timezone.datetime(year=end_year, month=8, day=19)
        return queryset.filter(datetime_encodage__gt=start, datetime_encodage__lt=end)


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
                classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
                try:
                    queryset = self.queryset.filter(student__classe__in=classes)
                except FieldError:
                    queryset = self.queryset.filter(matricule__classe__in=classes)
                    warnings.warn("Use *student* as field name instead of matricule", DeprecationWarning)
                return queryset
            except ObjectDoesNotExist:
                return self.queryset.none()

    def perform_create(self, serializer):
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
    permission_classes = (IsAuthenticated, IsSecretaryPermission)

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


class TeachingViewSet(ReadOnlyModelViewSet):
    queryset = TeachingModel.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = (IsAuthenticated,)


class EmailViewSet(ReadOnlyModelViewSet):
    queryset = EmailModel.objects.all().order_by("display")
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)
