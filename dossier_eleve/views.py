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

from django_weasyprint import WeasyTemplateView

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group

from django_filters import rest_framework as filters

# from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
# from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from core.views import BaseFilters, BaseModelViewSet, get_app_settings, BaseUploadFileView, get_core_settings
from core.utilities import get_menu
from core.utilities import get_scholar_year, check_student_photo
from core.models import StudentModel, ResponsibleModel
from core.people import People, get_classes

from .serializers import *
from .models import *
from .tasks import task_send_info_email, notify_sanction

from z3c.rml import rml2pdf
from io import BytesIO
from PyPDF2 import PdfFileMerger


def get_menu_entry(active_app, request):
    if (
        not request.user.has_perm("dossier_eleve.view_caseleve")
        and not request.user.has_perm("dossier_eleve.ask_sanction")
        and not request.user.has_perm("dossier_eleve.set_sanction")
    ):
        return {}

    has_only_ask = not request.user.has_perm("dossier_eleve.view_caseleve") \
        and request.user.has_perm("dossier_eleve.ask_sanction")
    menu_entry = {
        "app": "dossier_eleve",
        "display": "Dossier élèves",
        "url": "/dossier_eleve/ask_sanctions" if has_only_ask else "/dossier_eleve/",
        "active": active_app == "dossier_eleve",
    }
    last_access = request.session.get("dossier_eleve_last_access", None)
    if last_access:
        view_set = CasEleveViewSet.as_view({'get': 'list'})
        results = [c["id"] for c in view_set(request).data['results']]
        menu_entry["new_items"] = CasEleve.objects.filter(id__in=results, datetime_modified__gt=last_access).count()
        if menu_entry["new_items"] == 20:
            menu_entry["new_items"] = "20+"
    return menu_entry


def get_settings():
    return get_app_settings(DossierEleveSettingsModel)


def get_generic_groups() -> dict:
    sysadmin_group = Group.objects.get(name=settings.SYSADMIN_GROUP)
    direction_group = Group.objects.get(name=settings.DIRECTION_GROUP)
    coord_group = Group.objects.get(name=settings.COORDONATOR_GROUP)
    educ_group = Group.objects.get(name=settings.EDUCATOR_GROUP)
    teacher_group = Group.objects.get(name=settings.TEACHER_GROUP)
    pms_group = Group.objects.get(name=settings.PMS_GROUP)
    return {"sysadmin": sysadmin_group,
            "direction": direction_group,
            "coordonator": coord_group,
            "educator": educ_group,
            "teacher": teacher_group,
            "pms": pms_group,
            }


class BaseDossierEleveView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       TemplateView):
    filters = []

    def get_context_data(self, **kwargs):
        # Get settings.
        settings_dossier_eleve = get_settings()

        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context['settings'] = JSONRenderer().render(DossierEleveSettingsSerializer(settings_dossier_eleve).data).decode()
        context['menu'] = json.dumps(get_menu(self.request, "dossier_eleve"))
        context['filters'] = json.dumps(self.filters)
        scholar_year = get_scholar_year()
        context['current_year'] = json.dumps('%i-%i' % (scholar_year, scholar_year + 1))
        context['can_set_sanction'] = json.dumps(self.request.user.has_perm('dossier_eleve.set_sanction'))
        context['can_ask_sanction'] = json.dumps(self.request.user.has_perm('dossier_eleve.ask_sanction'))
        context['can_add_cas'] = json.dumps(self.request.user.has_perm('dossier_eleve.add_caseleve'))
        groups = get_generic_groups()
        groups["sysadmin"] = {"id": groups["sysadmin"].id, "text": "Admin"}
        groups["direction"] = {"id": groups["direction"].id, "text": "Direction"}
        groups["coordonator"] = {"id": groups["coordonator"].id, "text": "Coordonateur"}
        groups["educator"] = {"id": groups["educator"].id, "text": "Educateur"}
        groups["teacher"] = {"id": groups["teacher"].id, "text": "Professeurs"}
        groups["pms"] = {"id": groups["pms"].id, "text": "PMS"}
        context['groups'] = groups

        context["dossier_eleve_last_access"] = self.request.session.get("dossier_eleve_last_access", "")
        # Set last access
        self.request.session["dossier_eleve_last_access"] = timezone.now().isoformat()
        return context


class DossierEleveView(BaseDossierEleveView):
    template_name = "dossier_eleve/dossier_eleve.html"
    permission_required = ["dossier_eleve.view_caseleve"]
    filters = [
        {'value': 'matricule__display', 'text': 'Nom'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'info__info', 'text': 'Info'},
        {'value': 'sanction_decision__sanction_decision', 'text': 'Sanction/décision'},
        {'value': 'datetime_encodage', 'text': 'Date encodage'},
        {'value': 'datetime_sanction', 'text': 'Date sanction'},
        {'value': 'activate_important', 'text': 'Important'},
        {'value': 'matricule_id', 'text': 'Matricule'},
        {'value': 'scholar_year', 'text': 'Année scolaire'},
    ]


class CasEleveFilter(BaseFilters):
    student_field = "matricule"

    classe = filters.CharFilter(method='classe_by')
    activate_important = filters.BooleanFilter(field_name="important")
    no_sanctions = filters.BooleanFilter(method="no_sanctions_by")
    no_infos = filters.BooleanFilter(method="no_infos_by")
    matricule__display = filters.CharFilter(method="people_name_by")

    class Meta:
        fields_to_filter = ('matricule_id', 'info__info', 'sanction_decision__sanction_decision',
                            'datetime_encodage', "datetime_sanction")
        model = CasEleve
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def no_infos_by(self, queryset, field_name, value):
        if value:
            return queryset.filter(sanction_decision__isnull=False)
        else:
            return queryset

    def no_sanctions_by(self, queryset, field_name, value):
        if value:
            return queryset.filter(info__isnull=False)
        else:
            return queryset


class VisibilityPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        # groups = request.user.groups
        if request.user.groups.intersection(obj.visible_by_groups.all()).exists():
            return True

        return False


class CasEleveViewSet(BaseModelViewSet):
    queryset = CasEleve.objects.filter(matricule__isnull=False).order_by("-datetime_modified")

    serializer_class = CasEleveSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = CasEleveFilter
    ordering_fields = ('datetime_encodage', "matricule__last_name", "datetime_modified")
    user_field = 'created_by'

    def get_group_all_access(self):
        return get_settings().all_access.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if get_settings().enable_submit_sanctions:
            queryset = queryset.filter(Q(info__isnull=False) | ~Q(sanction_faite=False))

        filter_by_groups = Q()
        for g in self.request.user.groups.all():
            filter_by_groups |= Q(visible_by_groups=g)
        filter_by_groups |= Q(created_by=self.request.user)
        # Give access to tenures
        try:
            resp = ResponsibleModel.objects.get(user=self.request.user)
            filter_by_groups |= Q(matricule__classe__in=resp.tenure.all(), visible_by_tenure=True)
        except ObjectDoesNotExist:
            pass

        queryset = queryset.filter(filter_by_groups).distinct()
        return queryset

    def perform_create(self, serializer):
        send_to_teachers = serializer.validated_data.get("send_to_teachers", False)
        # Remove from serializer as model doesn't need it.
        if "send_to_teachers" in serializer.validated_data:
            serializer.validated_data.pop('send_to_teachers')

        super().perform_create(serializer)
        cas = serializer.save(created_by=self.request.user)
        if send_to_teachers:
            task_send_info_email.apply_async(
                countdown=1,
                kwargs={'instance_id': serializer.save().id}
            )

        if cas.sanction_decision:
            if cas.sanction_decision.notify:
                notify_sanction.apply_async(
                    countdown=1,
                    kwargs={"instance_id": cas.id}
                )

        if serializer.validated_data["info"]:
            self.force_visibility(serializer)
        else:
            serializer.save(visible_by_groups=get_generic_groups().values())

    def perform_update(self, serializer):
        super().perform_update(serializer)

        if serializer.validated_data['send_to_teachers']:
            task_send_info_email.apply_async(
                countdown=1,
                kwargs={'instance_id': serializer.save().id}
            )

        if serializer.validated_data["info"]:
            self.force_visibility(serializer)
        else:
            serializer.save(visible_by_groups=get_generic_groups().values())

    def force_visibility(self, serializer):
        user_groups = self.request.user.groups.all()
        dossier_settings = get_settings()

        visible_by_tenure = serializer.validated_data["visible_by_tenure"]
        if user_groups.filter(name=settings.SYSADMIN_GROUP):
            # Don't force for sysadmin.
            forced_visibility = []
        else:
            groups = get_generic_groups()
            # Match between groups and settings name.
            group_settings_match = {
                settings.DIRECTION_GROUP: "dir",
                settings.EDUCATOR_GROUP: "educ",
                settings.TEACHER_GROUP: "teacher",
                settings.PMS_GROUP: "pms",
                settings.COORDONATOR_GROUP: "coord",
            }

            considered_groups = [u_g for u_g in user_groups if u_g in groups.values()]
            concerned_settings = [
                {
                    "group": g.id,
                    "is_allowed": set(getattr(
                        dossier_settings, group_settings_match[g.name] + "_allow_visibility_to"
                    ).all().values_list("id", flat=True)),
                    "is_forced": set(getattr(
                        dossier_settings, group_settings_match[g.name] + "_force_visibility_to"
                    ).all().values_list("id", flat=True)),
                }
                for g in considered_groups
                ]

            # Complete group.
            for g in dossier_settings.tenure_force_visibility_from.all():
                group_index = next(
                    (i for i, group in enumerate(concerned_settings) if group["group"] == g.id),
                    None
                )
                if group_index is None:
                    continue
                concerned_settings[group_index]["is_forced"].add(-1)
            for g in dossier_settings.tenure_allow_visibility_from.all():
                group_index = next(
                    (i for i, group in enumerate(concerned_settings) if group["group"] == g.id),
                    None
                )
                if group_index is None:
                    continue
                concerned_settings[group_index]["is_allowed"].add(-1)

            try:
                responsible = ResponsibleModel.objects.get(user=self.request.user)
                if responsible.tenure.filter(id=serializer.instance.matricule.classe.id).exists():
                    concerned_settings.append(
                        {
                            "group": -1,
                            "is_allowed": set(
                                dossier_settings.tenure_allow_visibility_to.all().values_list("id", flat=True)
                            ),
                            "is_forced": set(
                                dossier_settings.tenure_force_visibility_to.all().values_list("id", flat=True)
                            )
                        }
                    )
            except ObjectDoesNotExist:
                pass

            # Concatenate all forced groups.
            forced_groups = {g for group in concerned_settings for g in group["is_forced"]}

            could_be_forced_perm = set()
            for c_s in concerned_settings:
                # It should be in allowed and forced simultaneously or only in forced.
                could_be_forced_perm = could_be_forced_perm.union(
                    c_s["is_allowed"].intersection(c_s["is_forced"]).union(
                        c_s["is_forced"].difference(c_s["is_allowed"])
                    )
                )

            only_allowed_perm = set()
            for c_s in concerned_settings:
                only_allowed_perm = only_allowed_perm.union(c_s["is_allowed"].difference(c_s["is_forced"]))

            forced_visibility = [
                f_g
                for f_g in forced_groups
                if f_g not in only_allowed_perm and f_g in could_be_forced_perm
            ]

            has_tenure = -1 in forced_visibility
            if has_tenure:
                forced_visibility.remove(-1)
                visible_by_tenure = True
            forced_visibility = Group.objects.filter(id__in=forced_visibility)

        visible_by = serializer.validated_data["visible_by_groups"] + list(forced_visibility)

        serializer.save(visible_by_groups=visible_by, visible_by_tenure=visible_by_tenure)

    def is_only_tenure(self):
        return False


class AskSanctionsView(BaseDossierEleveView):
    template_name = "dossier_eleve/ask_sanctions.html"
    permission_required = ["dossier_eleve.ask_sanction", "dossier_eleve.set_sanction"]
    filters = [
        {'value': 'matricule__display', 'text': 'Nom'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'sanction_decision__sanction_decision', 'text': 'Sanction/décision'},
        {'value': 'datetime_sanction', 'text': 'Date sanction'},
        {'value': 'datetime_conseil', 'text': 'Date du conseil'},
        {'value': 'datetime_encodage', 'text': 'Date encodage'},
        {'value': 'matricule_id', 'text': 'Matricule'},
        {'value': 'scholar_year', 'text': 'Année scolaire'},
        {'value': 'activate_all_retenues', 'text': 'Toutes les retenues'},
        {'value': 'activate_not_done', 'text': 'Sanctions non faites'},
        {'value': 'activate_waiting', 'text': 'En attente de validation'},
        {'value': 'activate_today', 'text': 'Sanction du jour'},
    ]

    def has_permission(self) -> bool:
        permissions = self.get_permission_required()
        for p in permissions:
            if self.request.user.has_perm(p):
                return True
        return False


class AskSanctionsFilter(BaseFilters):
    student_field = "matricule"

    classe = filters.CharFilter(method='classe_by')
    activate_not_done = filters.CharFilter(method='activate_not_done_by')
    activate_waiting = filters.CharFilter(method='activate_waiting_by')
    activate_today = filters.CharFilter(method="activate_today_by")
    matricule__display = filters.CharFilter(method="people_name_by")

    class Meta:
        fields_to_filter = ('matricule_id', 'sanction_decision__sanction_decision', 'datetime_sanction',
                            'datetime_conseil', 'datetime_encodage', 'sanction_decision__is_retenue')
        model = CasEleve
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, name, value):
        if not value[0].isdigit():
            return queryset

        all_access = get_settings().all_access.all()
        if not self.request.user.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
            queryset = queryset.filter(matricule__classe__in=classes)

        if len(value) > 0:
            queryset = queryset.filter(matricule__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(matricule__classe__letter=value[1].lower())
        return queryset

    def activate_not_done_by(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(datetime_sanction__lt=timezone.now())
        return queryset

    def activate_waiting_by(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(datetime_conseil__isnull=True, datetime_sanction__isnull=True)
        return queryset

    def activate_today_by(self, queryset, name, value):
        today = timezone.now()
        if value == "true":
            return queryset.filter(
                datetime_sanction__day=today.day,
                datetime_sanction__month=today.month,
                datetime_sanction__year=today.year
            )
        return queryset


class AskSanctionsViewSet(BaseModelViewSet):
    queryset = CasEleve.objects.filter(matricule__isnull=False, sanction_decision__isnull=False, sanction_faite=False)
    serializer_class = CasEleveSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = AskSanctionsFilter
    ordering_fields = ('datetime_encodage', 'datetime_sanction', 'matricule__classe__year',
                       'matricule__classe__letter', 'matricule__last_name')
    user_field = 'created_by'

    def get_queryset(self):
        sanctions = SanctionDecisionDisciplinaire.objects.filter(can_ask=True)
        if self.request.GET.get("activate_all_retenues", None):
            return CasEleve.objects.filter(
                matricule__isnull=False,
                sanction_decision__is_retenue=True,
                sanction_faite=False,
            )

        queryset = super().get_queryset().filter(sanction_decision__in=sanctions)
        return queryset

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.save(sanction_faite=False)
        cas = serializer.save(visible_by_groups=get_generic_groups().values())

        if cas.sanction_decision:
            if cas.sanction_decision.notify:
                notify_sanction.apply_async(
                    countdown=1,
                    kwargs={"instance_id": cas.id}
                )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        serializer.save(visible_by_groups=get_generic_groups().values())


class InfoViewSet(ReadOnlyModelViewSet):
    queryset = InfoEleve.objects.all()
    serializer_class = InfoEleveSerializer


class SanctionDecisionViewSet(ReadOnlyModelViewSet):
    queryset = SanctionDecisionDisciplinaire.objects.order_by("sanction_decision")
    serializer_class = SanctionDecisionDisciplinaireSerializer

    def get_queryset(self):
        self.queryset = super().get_queryset()
        only_sanctions = self.request.GET.get('only_sanctions', 0) == "1"
        if only_sanctions:
            return self.queryset.filter(can_ask=True)

        return self.queryset


class StatisticAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, matricule, format=None):
        only_sanctions = request.GET.get('only_sanctions', 1) == 1
        stats = self.gen_stats(request.user, matricule, only_sanctions)
        return Response(json.dumps(stats))

    def gen_stats(self, user_from, matricule, only_sanctions=False, all_years=False):
        all_access = get_settings().all_access.all()
        queryset = CasEleve.objects.all()
        if not user_from.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=user_from).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, user_from)
            queryset = queryset.filter(matricule__classe__in=classes)

        cas_discip = queryset.filter(info=None, matricule=matricule)\
                             .filter(Q(sanction_faite=True) | Q(sanction_faite__isnull=True))
        cas_info = queryset.filter(sanction_decision=None, matricule=matricule)

        if not all_years:
            current_scolar_year = get_scholar_year()
            limit_date = timezone.make_aware(timezone.datetime(current_scolar_year, 8, 15))
            cas_discip = cas_discip.filter(datetime_encodage__gte=limit_date)
            cas_info = cas_info.filter(datetime_encodage__gte=limit_date)

        sanctions = SanctionStatisticsModel.objects.all()

        stats = []
        for s in sanctions:
            stat = {
                'display': s.display,
                'value': len(cas_discip.filter(sanction_decision__in=s.sanctions_decisions.all()))
            }
            stats.append(stat)

        if not only_sanctions:
            stats.append({'display': 'Non disciplinaire', 'value': len(cas_info)})
            stats.append({'display': 'Total disciplinaire', 'value': len(cas_discip)})

        return stats


class UploadFileView(BaseUploadFileView):
    file_model = CasAttachment
    file_serializer = CasAttachmentSerializer


class AttachmentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, year=None, month=None, day=None, file=None, pk=None, format=None):
        try:
            if pk:
                attachment = CasAttachment.objects.get(pk=pk)
            else:
                attachment = CasAttachment.objects.get(attachment__exact=f"dossier_eleve/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}/{file}")
            queryset = CasEleve.objects.filter(attachments=attachment)
            filter_by_groups = Q()
            for g in request.user.groups.all():
                filter_by_groups |= Q(visible_by_groups=g)
            filter_by_groups |= Q(created_by=request.user)
            resp = ResponsibleModel.objects.get(user=request.user)
            filter_by_groups |= Q(matricule__classe__in=resp.tenure.all(), visible_by_tenure=True)
            queryset = queryset.filter(filter_by_groups).distinct()
            if not queryset.exists():
                return HttpResponse(status=404)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

        response = HttpResponse(attachment.attachment)
        response["Content-Disposition"] = f'attachment; filename="{file if file else attachment.attachment.name}"'

        return response


class CasEleveListPDFGen(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    WeasyTemplateView
):
    permission_required = ["dossier_eleve.view_caseleve"]
    template_name = "dossier_eleve/cas_list_pdf.html"

    def get_context_data(self, **kwargs) -> dict:
        view_set = CasEleveViewSet.as_view({'get': 'list'})
        results = [c["id"] for c in view_set(self.request).data['results']]
        results = CasEleve.objects.filter(id__in=results)
        context = {'list': results}
        return context

    def modify_entries(self, results):
        return results


class CasElevePDFGenAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if request.GET.get('matricule_id'):
            pdf = self.create_pdf(request)
            if not pdf:
                return render(request, 'dossier_eleve/no_student.html')
            pdf_name = str(request.GET['matricule_id']) + '.pdf'

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
            response.write(pdf.read())
            return response

        if request.GET.get('classe'):
            classe_access = get_classes(get_settings().teachings.all(), True, request.user)
            try:
                classe = classe_access.get(id=request.GET['classe'])
            except ObjectDoesNotExist:
                return HttpResponse("Vous n'avez pas les accès nécessaire.", status=401)

            students = People().get_students_by_classe(classe)
            merger = PdfFileMerger()
            added = False
            for s in students:
                request._request.GET = request.GET.copy()
                request._request.GET['matricule_id'] = s.matricule
                pdf = self.create_pdf(request)
                if not pdf:
                    continue

                merger.append(pdf)
                added = True

            if not added:
                return render(request, 'dossier_eleve/no_student.html')

            output_stream = BytesIO()
            merger.write(output_stream)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename; filename="' + classe.compact_str + '.pdf"'
            response.write(output_stream.getvalue())
            return response

        return render(request, 'dossier_eleve/no_student.html')

    @staticmethod
    def create_pdf(request):
        if request._request.GET.get('classe'):
            request._request.GET.pop('classe')
        view_set = CasEleveViewSet.as_view({'get': 'list'})
        results = view_set(request._request).data['results']
        if not results:
            return None

        # Use datetime object instead of plain text.
        for r in results:
            r['datetime_encodage'] = timezone.datetime.strptime(r['datetime_encodage'][:19], "%Y-%m-%dT%H:%M:%S")
            if r['info']:
                continue
            r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'][:19], "%Y-%m-%dT%H:%M:%S") if r['datetime_sanction'] else None
        student = StudentModel.objects.get(matricule=request.GET['matricule_id'])
        check_student_photo(student)
        #TODO: Should we show current year statistics or all years statistics?
        context = {'statistics': StatisticAPI().gen_stats(request.user, student,
                                                          all_years=False)}
        tenure = ResponsibleModel.objects.filter(tenure=student.classe).first()
        context['tenure'] = tenure.fullname if tenure else "—"

        context['student'] = student
        context['list'] = results
        context['absolute_path'] = settings.BASE_DIR

        t = get_template('dossier_eleve/discip_pdf.rml')
        rml_str = t.render(context)

        pdf = rml2pdf.parseString(rml_str)
        return pdf


class AskSanctionsPDFGenAPI(APIView):
    permission_classes = (IsAuthenticated,)
    template = ""
    file_name = ""
    field_date = ""

    def get(self, request, format=None):
        view_set = AskSanctionsViewSet.as_view({'get': 'list'})
        results = view_set(request._request).data['results']
        results = self.modify_entries(results)

        date_from = request.GET.get('datetime_%s__gt' % self.field_date)
        date_to = request.GET.get('datetime_%s__lt' % self.field_date)
        context = {'date_from': date_from, 'date_to': date_to,
                   'list': results}
        t = get_template(self.template)
        rml_str = t.render(context)

        pdf = rml2pdf.parseString(rml_str)
        if not pdf:
            return render(request, 'dossier_eleve/no_student.html')
        pdf_name = self.file_name + '_' + date_from + '_' + date_to + '.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
        response.write(pdf.read())
        return response

    def modify_entries(self, results):
        return results


class AskSanctionCouncilPDFGenAPI(AskSanctionsPDFGenAPI):
    template = "dossier_eleve/discip_council.rml"
    file_name = "council"
    field_date = "conseil"

    def modify_entries(self, results):
        for r in results:
            if r['datetime_sanction']:
                r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'][:19],
                                                                    "%Y-%m-%dT%H:%M:%S")
            else:
                r['datetime_sanction'] = None
            r['datetime_conseil'] = timezone.datetime.strptime(r['datetime_conseil'][:19],
                                                               "%Y-%m-%dT%H:%M:%S")
        return results


class AskSanctionRetenuesPDFGenAPI(AskSanctionsPDFGenAPI):
    template = "dossier_eleve/discip_retenues.rml"
    file_name = "retenues"
    field_date = "sanction"

    def modify_entries(self, results):
        for r in results:
            r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'][:19],
                                                                "%Y-%m-%dT%H:%M:%S")
            if r["time_sanction_end"]:
                r["time_sanction_end"] = r["time_sanction_end"][:5]
        return results


class RetenuePDF(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    WeasyTemplateView
):
    permission_required = ['dossier_eleve.ask_sanction', 'dossier_eleve.view_caseleve']
    template_name = "dossier_eleve/retenue_pdf.html"

    def get_context_data(self, sanction, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["sanction"] = CasEleve.objects.get(id=sanction)
        context["core_settings"] = get_core_settings()
        return context
