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

from dateutil.relativedelta import relativedelta

from django_weasyprint import WeasyTemplateView

from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter

from core.views import BaseFilters, PageNumberSizePagination
from core.utilities import get_menu
from core import email

from .models import Absence, AbsenceProfSettingsModel, MotifAbsence
from .serializers import AbsenceProfSettingsSerializer, AbsenceProfSerializer, MotifAbsenceSerializer


def get_menu_entry(active_app, user):
    if not user.has_perm('absence_prof.access_absences'):
        return {}
    return {
            "app": "absence_prof",
            "display": "Abs. Profs",
            "url": "/absence_prof/",
            "active": active_app == "absence_prof"
    }


def get_settings():
    settings_absence_prof = AbsenceProfSettingsModel.objects.first()
    if not settings_absence_prof:
        # Create default settings.
        settings_absence_prof = AbsenceProfSettingsModel.objects.create().save()

    return settings_absence_prof


class AbsenceProfView(LoginRequiredMixin,
                      PermissionRequiredMixin,
                      TemplateView):
    template_name = "absence_prof/absence_prof.html"
    permission_required = ('absence_prof.access_absences')
    filters = [{'value': 'name', 'text': 'Nom'},
               {'value': 'activate_ongoing', 'text': 'Absences courantes'},
               {'value': 'date_range', 'text': 'Absences pendant une période'},
               {'value': 'date_month', 'text': 'Absences par mois'},
               # {'value': 'matricule_id', 'text': 'Matricule'},
               ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "absence_prof"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((AbsenceProfSettingsSerializer(get_settings()).data))

        return context


class AbsenceProfFilter(BaseFilters):
    activate_ongoing = filters.BooleanFilter(method="activate_ongoing_by")
    date_month__gte = filters.CharFilter(method="date_month__gte_by")
    date_month__lte = filters.CharFilter(method="date_month__lte_by")
    date_range__gte = filters.CharFilter(method="date_range__gte_by")
    date_range__lte = filters.CharFilter(method="date_range__lte_by")

    class Meta:
        fields_to_filter = ('activate_ongoing', 'date_month__gte', 'date_month__lte', 'name', 'date_range__gte', 'date_range__lte',)
        model = Absence
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_ongoing_by(self, queryset, name, value):
        return queryset.filter(datetime_absence_end__gt=timezone.now() - relativedelta(days=1))

    def date_month__gte_by(self, queryset, name, value):
        return queryset.filter(datetime_absence_end__month__gte=int(value[5:]),
                               datetime_absence_end__year__gte=int(value[:4]))

    def date_month__lte_by(self, queryset, name, value):
        return queryset.filter(datetime_absence_start__month__lte=int(value[5:]),
                               datetime_absence_start__year__lte=int(value[:4]))

    def date_range__gte_by(self, queryset, name, value):
        for a in queryset.filter(datetime_absence_end__lte=value):
            print("%s: %s - %s" % (a.name, a.datetime_absence_start, a.datetime_absence_end))
        return queryset.filter(datetime_absence_end__gte=value)

    def date_range__lte_by(self, queryset, name, value):
        return queryset.filter(datetime_absence_start__lte=value)


class AbsenceProfViewSet(ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceProfSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = AbsenceProfFilter
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    pagination_class = PageNumberSizePagination
    # ordering_fields = ('',)

    def perform_create(self, serializer):
        # Override user save.
        p = serializer.save(user=self.request.user.username)
        self.send_emails(p, "[Absence prof] Nouvelle absence", True)

    def perform_update(self, serializer):
        p = serializer.save(user=self.request.user.username)
        self.send_emails(p, "[Absence prof] Modification de l'absence", False)

    def send_emails(self, instance, subject, is_new):
        """Send an email to notify new absence and change."""
        context = {'absence': instance, 'new': is_new}
        email.send_email(to=[], subject=subject,
                         email_template='absence_prof/email.html', context=context)


class MotifAbsenceViewSet(ReadOnlyModelViewSet):
    queryset = MotifAbsence.objects.all()
    serializer_class = MotifAbsenceSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)


class ListPDF(LoginRequiredMixin,
                        #    PermissionRequiredMixin,
              WeasyTemplateView):
    # permission_required = ('absence_prof.access_dossier_eleve')
    template_name = "absence_prof/list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        view_set = AbsenceProfViewSet.as_view({'get': 'list'})
        absences = view_set(self.request).data['results']
        for a in absences:
            a['datetime_absence_start'] = timezone.datetime.strptime(a['datetime_absence_start'][:10], "%Y-%m-%d")
            a['datetime_absence_end'] = timezone.datetime.strptime(a['datetime_absence_end'][:10], "%Y-%m-%d")
        context['absences'] = absences
        return context
