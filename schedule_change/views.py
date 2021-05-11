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

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import F, Q

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED

from django_filters import rest_framework as filters

from core.views import BaseModelViewSet, BaseFilters, get_core_settings, get_app_settings
from core.utilities import get_menu
from core.email import send_email

from .models import ScheduleChangeSettingsModel, ScheduleChangeModel, ScheduleChangeTypeModel, ScheduleChangePlaceModel,\
    ScheduleChangeCategoryModel
from .tasks import task_export
from .serializers import ScheduleChangeSettingsSerializer, ScheduleChangeSerializer, ScheduleChangeTypeSerializer,\
    ScheduleChangePlaceSerializer, ScheduleChangeCategorySerializer


def get_menu_entry(active_app: str, request) -> dict:
    if not request.user.has_perm('schedule_change.view_schedulechangemodel'):
        return {}
    return {
            "app": "schedule_change",
            "display": "Changement Horaire",
            "url": "/schedule_change",
            "active": active_app == "schedule_change"
    }


def get_settings():
    # Ensure core settings is created.
    get_core_settings()
    return get_app_settings(ScheduleChangeSettingsModel)


class ScheduleChangeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "schedule_change/schedule_change.html"
    permission_required = ('schedule_change.view_schedulechangemodel')
    filters = [{'value': 'activate_ongoing', 'text': 'Prochains changements'},
               {'value': 'date_change', 'text': "Date du changement"},
               {'value': 'activate_has_classe', 'text': 'Concerne une classe'},
               ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request, "schedule_change"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((ScheduleChangeSettingsSerializer(get_settings()).data))
        context['can_add'] = json.dumps(self.request.user.has_perm('schedule_change.add_schedulechangemodel'))
        return context


class ScheduleChangeViewReadOnly(TemplateView):
    template_name = "schedule_change/schedule_change.html"
    filters = [{'value': 'activate_ongoing', 'text': 'Prochains changements'},
               {'value': 'date_change', 'text': "Date du changement"},
               {'value': 'activate_has_classe', 'text': 'Concerne une classe'},
               ]

    def dispatch(self, request, *args, **kwargs):
        if not get_settings().enable_fullscreen:
            return HttpResponse(status=403)
        return super().dispatch(request, *args, *kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps({})
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((ScheduleChangeSettingsSerializer(get_settings()).data))
        context['can_add'] = json.dumps(False)
        return context


class ScheduleChangeFilter(BaseFilters):
    activate_ongoing = filters.BooleanFilter(method="activate_ongoing_by")
    activate_has_classe = filters.BooleanFilter(method="activate_has_classe_by")
    activate_show_for_students = filters.BooleanFilter(method="activate_show_for_students_by")

    class Meta:
        fields_to_filter = ["date_change"]
        model = ScheduleChangeModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_ongoing_by(self, queryset, name, value):
        now = timezone.now()
        return queryset.filter(
            Q(date_change=now.date(), time_start=None, time_end=None)
            | Q(date_change=now.date(), time_end__hour__gte=now.astimezone().hour)
            | Q(date_change=now.date(), time_start__hour__gte=now.astimezone().hour, time_end=None)
            | Q(date_change__gt=now)
        )

    def activate_has_classe_by(self, queryset, name, value):
        return queryset.exclude(classes__exact="")

    def activate_show_for_students_by(self, queryset, name, value):
        return queryset.exclude(hide_for_students=True)


class ScheduleChangeTypeViewSet(ReadOnlyModelViewSet):
    queryset = ScheduleChangeTypeModel.objects.all()
    serializer_class = ScheduleChangeTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ScheduleChangeCategoryViewSet(ReadOnlyModelViewSet):
    queryset = ScheduleChangeCategoryModel.objects.all()
    serializer_class = ScheduleChangeCategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ScheduleChangePlaceViewSet(ReadOnlyModelViewSet):
    queryset = ScheduleChangePlaceModel.objects.all()
    serializer_class = ScheduleChangePlaceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ScheduleChangeViewSet(BaseModelViewSet):
    queryset = ScheduleChangeModel.objects.all().order_by(
        'date_change',
        F('time_start').asc(nulls_first=True),
        'time_end',
        "place",
    )
    serializer_class = ScheduleChangeSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_class = ScheduleChangeFilter

    def perform_create(self, serializer):
        email_general = serializer.validated_data.pop('send_email_general')
        email_substitute = serializer.validated_data.pop('send_email_substitute')
        super().perform_create(serializer)
        change = serializer.save()
        self.notify_email(change, email_general, email_substitute, "Nouveau changement")
        if get_settings().copy_to_remote:
            self.copy_to_remote(requests.post, change.id)

    def perform_update(self, serializer):
        email_general = serializer.validated_data.pop('send_email_general')
        email_substitute = serializer.validated_data.pop('send_email_substitute')
        super().perform_update(serializer)
        change = serializer.save()
        self.notify_email(change, email_general, email_substitute, "Changement modifié")
        if get_settings().copy_to_remote:
            self.copy_to_remote(requests.put, change.id)

    def perform_destroy(self, instance):
        if get_settings().copy_to_remote:
            self.copy_to_remote(requests.delete, instance.id)
        super().perform_destroy(instance)

    def copy_to_remote(self, method, id):
        core_settings = get_core_settings()
        remote_url = core_settings.remote
        # Ensure a slash at the end.
        if remote_url[-1] != '/':
            remote_url += '/'
        remote_url += 'schedule_change/api/schedule_change/'
        if method != requests.post:
            remote_url += '%i/' % id
        remote_token = core_settings.remote_token
        headers = {'Authorization': 'Token %s' % remote_token}
        self.request.data['id'] = id
        method(remote_url, headers=headers, json=self.request.data)

    def notify_email(self, change, email_general, email_substitute, title):
        if email_general:
            recipients = map(lambda e: e.email, get_settings().notify_by_email_to.all())
            send_email(to=recipients, subject="[Changement horaire] %s" % title,
                       email_template="schedule_change/email.html",
                       context={"change": change})
        if email_substitute and change.teachers_substitute.all():
            email_school = get_settings().email_school
            recipients = map(lambda t: t.email_school if email_school else t.email, change.teachers_substitute.all())
            recipients = filter(lambda r: r is not None, recipients)
            send_email(to=recipients, subject="[Changement horaire] %s" % title,
                       email_template="schedule_change/email.html",
                       context={"change": change})

    def get_queryset(self):
        return self.queryset

    def get_group_all_access(self):
        return get_settings().all_access.all()


class SummaryPDFAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None) -> Response:
        view_set = ScheduleChangeViewSet.as_view({'get': 'list'})
        results = view_set(request._request).data['results']
        changes = [c['id'] for c in results]

        date_from = request.GET.get('date_change__gte')
        date_to = request.GET.get('date_change__lte')
        send_to_teachers = json.loads(request.GET.get('send_to_teachers', 'false'))
        message = request.GET.get('message', "")

        task = task_export.delay(changes, date_from, date_to, send_to_teachers, message)

        return Response(status=HTTP_202_ACCEPTED, data=json.dumps(str(task)))
