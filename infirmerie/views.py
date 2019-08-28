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
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from .models import Passage, InfirmerieSettingsModel

from core.people import People
from core import email
from core.utilities import get_menu, check_student_photo

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from core.views import BaseModelViewSet, BaseFilters
from .serializers import PassageSerializer, InfirmerieSettingsSerializer


def get_menu_entry(active_app, user):
    if not user.has_perm('infirmerie.access_infirmerie'):
        return {}
    return {
            "app": "infirmerie",
            "display": "Infirmerie",
            "url": "/infirmerie",
            "active": active_app == "infirmerie"
    }


def get_settings():
    settings_infirmerie = InfirmerieSettingsModel.objects.first()
    if not settings_infirmerie:
        # Create default settings.
        settings_infirmerie = InfirmerieSettingsModel.objects.create().save()

    return settings_infirmerie


def send_emails(passage, template, subject):
    eleve = People().get_student_by_id(passage.matricule.matricule)
    if check_student_photo(eleve, copy=False):
        image = static("/photos/" + str(passage.matricule.matricule) + ".jpg")
    else:
        image = static("/photos/unknown.jpg")

    context = {'eleve': eleve, 'heure_arrive': passage.datetime_arrive,
               'commentaire': passage.motifs_admission, 'passage': passage,
               'phone_number': get_settings().phone_number}
    recipients = email.get_resp_emails(eleve)
    recipients_emails = []
    for r in recipients.items():
        recipients_emails.append(r[0])

    if not settings.DEBUG:
        email.send_email(to=recipients, subject="[Infirmerie] %s %s %s" % (subject, eleve.fullname, eleve.classe.compact_str),
                         email_template="infirmerie/" + template + ".html", context=context, images=[image])
    else:
        print("Sending to: " + str(recipients_emails))
        email.send_email(to=[settings.EMAIL_ADMIN], subject="[Infirmerie] %s %s %s" % (subject, eleve.fullname, eleve.classe.compact_str),
                         email_template="infirmerie/" + template + ".html", context=context, images=[image])


class PassageView(LoginRequiredMixin,
                 PermissionRequiredMixin,
                 TemplateView):
    template_name = "infirmerie/infirmerie.html"
    permission_required = ('infirmerie.access_infirmerie')
    filters = [{'value': 'name', 'text': 'Nom'},
               {'value': 'activate_ongoing', 'text': 'Malades présents'},
               {'value': 'matricule_id', 'text': 'Matricule'},]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request.user, "infirmerie"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((InfirmerieSettingsSerializer(get_settings()).data))

        return context


class PassageFilter(BaseFilters):
    activate_ongoing = filters.BooleanFilter(method="activate_ongoing_by")

    class Meta:
        fields_to_filter = ('matricule_id', 'activate_ongoing',)
        model = Passage
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_ongoing_by(self, queryset, name, value):
        return queryset.filter(datetime_sortie__isnull=True)


class PassageViewSet(BaseModelViewSet):
    queryset = Passage.objects.filter(matricule__isnull=False)
    serializer_class = PassageSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = PassageFilter
    ordering_fields = ('datetime_arrive',)

    def perform_create(self, serializer):
        # Override user save.
        p = serializer.save()
        send_emails(p, "nouveau_email", "Arrivée de")

    def perform_update(self, serializer):
        p = serializer.save()
        if serializer.validated_data['datetime_sortie']:
            send_emails(p, "sortie_email", "Sortie de")
        else:
            send_emails(p, "nouveau_email", "[Mise à jour]Arrivée de")

    def get_group_all_access(self):
        return get_settings().all_access.all()
