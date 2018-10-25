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

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.utils import timezone
from django.db.models import F

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django_filters import rest_framework as filters

from core.views import BaseModelViewSet, BaseFilters
from core.utilities import get_menu
from core.email import send_email

from .models import ScheduleChangeSettingsModel, ScheduleChangeModel
from .serializers import ScheduleChangeSettingsSerializer, ScheduleChangeSerializer


def get_settings():
    settings_schedule = ScheduleChangeSettingsModel.objects.first()
    if not settings_schedule:
        # Create default settings.
        settings_schedule = ScheduleChangeSettingsModel.objects.create().save()

    return settings_schedule


class ScheduleChangeView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "schedule_change/schedule_change.html"
    permission_required = ('schedule_change.access_schedule_change')
    filters = [{'value': 'activate_ongoing', 'text': 'Prochains changements'},
               {'value': 'date_change', 'text': "Date du changement"},
               ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "schedule_change"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((ScheduleChangeSettingsSerializer(get_settings()).data))
        context['can_add'] = json.dumps(self.request.user.has_perm('schedule_change.add_schedulechangemodel'))

        return context


class ScheduleChangeFilter(BaseFilters):
    activate_ongoing = filters.BooleanFilter(method="activate_ongoing_by")

    class Meta:
        fields_to_filter = ('date_change', 'activate_ongoing')
        model = ScheduleChangeModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_ongoing_by(self, queryset, name, value):
        return queryset.filter(date_change__gte=timezone.now())


class ScheduleChangeViewSet(BaseModelViewSet):
    queryset = ScheduleChangeModel.objects.all().order_by('date_change', F('time_start').asc(nulls_first=True), 'time_end')
    serializer_class = ScheduleChangeSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = ScheduleChangeFilter

    def perform_create(self, serializer):
        email_general = serializer.validated_data.pop('send_email_general')
        email_substitute = serializer.validated_data.pop('send_email_substitute')
        super().perform_create(serializer)
        change = serializer.save()
        self.notify_email(change, email_general, email_substitute, "Nouveau changement")


    def perform_update(self, serializer):
        email_general = serializer.validated_data.pop('send_email_general')
        email_substitute = serializer.validated_data.pop('send_email_substitute')
        super().perform_update(serializer)
        change = serializer.save()
        self.notify_email(change, email_general, email_substitute, "Changement modifié")

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
