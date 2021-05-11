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

from django.templatetags.static import static
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from core import email
from core.people import People, get_classes
from core.views import BaseFilters, BaseModelViewSet, get_app_settings
from core.utilities import get_menu, check_student_photo

from .models import Appel, ObjectModel, MotiveModel, AppelsSettingsModel
from .serializers import AppelSerializer, ObjectSerializer, MotiveSerializer, AppelsSettingsSerializer


def get_menu_entry(active_app, request):
    if not request.user.has_perm('appels.view_appel'):
        return {}
    return {
            "app": "appels",
            "display": "Appels",
            "url": "/appels/",
            "active": active_app == "appels"
    }


def get_settings():
    return get_app_settings(AppelsSettingsModel)


def send_emails(appel):
    context = {'appel': appel}
    image = []
    name = appel.name
    if appel.is_student:
        student = People().get_student_by_id(appel.matricule.matricule)
        name = str(student)
        context['etudiant'] = student
        if check_student_photo(student, copy=False):
            image = [static("/photos/" + str(appel.matricule.matricule) + ".jpg")]
        else:
            image = [static("/photos/unknown.jpg")]

    sent_to = list(
        filter(lambda e: e != 'robot@isln.be', map(lambda e: e.email, appel.emails.all())))
    if appel.custom_email:
        sent_to.append(appel.custom_email)
    if not settings.DEBUG:
        email.send_email(to=sent_to, subject="[Appel] %s" % name,
                         email_template="appels/email.html", context=context, images=image)
    else:
        print(sent_to)
        email.send_email(to=[settings.EMAIL_ADMIN], subject="[Appel] %s" % name,
                         email_template="appels/email.html",
                         context=context, images=image)


class AppelsView(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 TemplateView):
    template_name = "appels/appels.html"
    permission_required = ('appels.view_appel')
    filters = [{'value': 'name', 'text': 'Nom'},
               {'value': 'datetime_appel', 'text': "Date d'appel"},
               {'value': 'matricule_id', 'text': 'Matricule'},
               {'value': 'activate_ongoing', 'text': 'Appels non traités'},]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request, "appels"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((AppelsSettingsSerializer(get_settings()).data))

        return context


class AppelFilter(BaseFilters):
    activate_ongoing = filters.BooleanFilter(method="activate_ongoing_by")

    class Meta:
        fields_to_filter = ('name', 'matricule_id', 'object', 'motive',
                            'datetime_motif_start', 'datetime_motif_end',
                            'datetime_appel', 'datetime_traitement',
                            'is_traiter',)
        model = Appel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_ongoing_by(self, queryset, name, value):
        return queryset.filter(is_traiter=False)


class AppelViewSet(BaseModelViewSet):
    queryset = Appel.objects.filter(Q(is_student=False) | Q(matricule__isnull=False))
    serializer_class = AppelSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = AppelFilter
    ordering_fields = ('name', 'datetime_appel', 'datetime_traitement', 'is_traiter')

    def perform_create(self, serializer):
        super().perform_create(serializer)
        # Set full name.
        if serializer.validated_data['is_student']:
            name = serializer.validated_data['matricule'].fullname
            serializer.save(name=name)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if serializer.validated_data['emails']:
            appel = serializer.save(datetime_traitement=timezone.now(), is_traiter=True)
            send_emails(appel)
        if serializer.validated_data['custom_email']:
            appel = serializer.save(datetime_traitement=timezone.now(), is_traiter=True)
            send_emails(appel)

    def get_group_all_access(self):
        return get_settings().all_access.all()


class MotiveViewSet(ReadOnlyModelViewSet):
    queryset = MotiveModel.objects.all()
    serializer_class = MotiveSerializer


class ObjectViewSet(ReadOnlyModelViewSet):
    queryset = ObjectModel.objects.all()
    serializer_class = ObjectSerializer
