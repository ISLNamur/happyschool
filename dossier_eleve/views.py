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
from weasyprint import HTML

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
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
from rest_framework.filters import OrderingFilter

# from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from core.views import (
    BaseFilters,
    BaseModelViewSet,
    get_app_settings,
    BaseUploadFileView,
    get_core_settings,
    BinaryFileRenderer,
    PageNumberSizePagination,
)
from core.utilities import get_menu
from core.utilities import get_scholar_year, check_student_photo
from core.models import StudentModel, ResponsibleModel, NotificationLogModel
from core.people import People, get_classes
from core.email import send_email, get_resp_emails

from .serializers import *
from .models import *
from .tasks import task_send_info_email, notify_sanction

from io import BytesIO
from PyPDF2 import PdfWriter


def get_menu_entry(active_app, request):
    if (
        not request.user.has_perm("dossier_eleve.view_caseleve")
        and not request.user.has_perm("dossier_eleve.ask_sanction")
        and not request.user.has_perm("dossier_eleve.set_sanction")
    ):
        return {}

    has_only_ask = not request.user.has_perm("dossier_eleve.view_caseleve") and (
        request.user.has_perm("dossier_eleve.ask_sanction")
        or request.user.has_perm("dossier_eleve.set_sanction")
    )

    menu_entry = {
        "app": "dossier_eleve",
        "display": "Dossier élèves",
        "url": "/dossier_eleve/ask_sanctions" if has_only_ask else "/dossier_eleve/",
        "active": active_app == "dossier_eleve",
    }
    last_access = request.session.get("dossier_eleve_last_access", None)
    if last_access:
        view_set = CasEleveViewSet.as_view({"get": "list"})
        results = [c["id"] for c in view_set(request).data["results"]]
        menu_entry["new_items"] = CasEleve.objects.filter(
            id__in=results, datetime_modified__gt=last_access
        ).count()
        if menu_entry["new_items"] >= 20:
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
    reception_group = Group.objects.get(name=settings.RECEPTION_GROUP)
    return {
        "sysadmin": sysadmin_group,
        "direction": direction_group,
        "coordonator": coord_group,
        "educator": educ_group,
        "teacher": teacher_group,
        "pms": pms_group,
        "reception": reception_group,
    }


class BaseDossierEleveView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    filters = []

    def get_context_data(self, **kwargs):
        # Get settings.
        settings_dossier_eleve = get_settings()

        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context["settings"] = (
            JSONRenderer()
            .render(DossierEleveSettingsSerializer(settings_dossier_eleve).data)
            .decode()
        )
        context["menu"] = json.dumps(get_menu(self.request, "dossier_eleve"))
        context["filters"] = json.dumps(self.filters)
        scholar_year = get_scholar_year()
        context["current_year"] = json.dumps("%i-%i" % (scholar_year, scholar_year + 1))
        context["can_set_sanction"] = json.dumps(
            self.request.user.has_perm("dossier_eleve.set_sanction")
        )
        context["can_ask_sanction"] = json.dumps(
            self.request.user.has_perm("dossier_eleve.ask_sanction")
        )
        context["can_add_cas"] = json.dumps(
            self.request.user.has_perm("dossier_eleve.add_caseleve")
        )
        groups = get_generic_groups()
        groups["sysadmin"] = {"id": groups["sysadmin"].id, "text": "Admin"}
        groups["direction"] = {"id": groups["direction"].id, "text": "Direction"}
        groups["coordonator"] = {"id": groups["coordonator"].id, "text": "Coordonateur"}
        groups["educator"] = {"id": groups["educator"].id, "text": "Educateur"}
        groups["teacher"] = {"id": groups["teacher"].id, "text": "Professeurs"}
        groups["pms"] = {"id": groups["pms"].id, "text": "PMS"}
        groups["reception"] = {"id": groups["reception"].id, "text": "Accueil"}
        context["groups"] = groups
        context["proeco"] = json.dumps("proeco" in settings.INSTALLED_APPS)

        context["dossier_eleve_last_access"] = self.request.session.get(
            "dossier_eleve_last_access", ""
        )
        # Set last access
        self.request.session["dossier_eleve_last_access"] = timezone.now().isoformat()
        return context


class DossierEleveView(BaseDossierEleveView):
    template_name = "dossier_eleve/dossier_eleve.html"
    permission_required = ["dossier_eleve.view_caseleve"]
    filters = [
        {"value": "student", "text": "Nom"},
        {"value": "classe", "text": "Classe"},
        {"value": "info__info", "text": "Info"},
        {"value": "sanction_decision__sanction_decision", "text": "Sanction/décision"},
        {"value": "datetime_encodage", "text": "Date encodage"},
        {"value": "date_sanction", "text": "Date sanction"},
        {"value": "activate_important", "text": "Important"},
        {"value": "student__matricule", "text": "Matricule"},
        {"value": "scholar_year", "text": "Année scolaire"},
    ]


class CasEleveFilter(BaseFilters):
    classe = filters.CharFilter(method="classe_by")
    student = filters.CharFilter(method="people_name_by")
    activate_important = filters.BooleanFilter(field_name="important")
    no_sanctions = filters.BooleanFilter(method="no_sanctions_by")
    no_infos = filters.BooleanFilter(method="no_infos_by")

    class Meta:
        fields_to_filter = (
            "student__matricule",
            "info__info",
            "sanction_decision__sanction_decision",
            "datetime_encodage",
            "date_sanction",
        )
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


class ForceVisibilityMixin:
    def force_visibility(self, serializer) -> CasEleve:
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
                    "is_allowed": set(
                        getattr(
                            dossier_settings, group_settings_match[g.name] + "_allow_visibility_to"
                        )
                        .all()
                        .values_list("id", flat=True)
                    ),
                    "is_forced": set(
                        getattr(
                            dossier_settings, group_settings_match[g.name] + "_force_visibility_to"
                        )
                        .all()
                        .values_list("id", flat=True)
                    ),
                }
                for g in considered_groups
            ]

            # Complete group.
            for g in dossier_settings.tenure_force_visibility_from.all():
                group_index = next(
                    (i for i, group in enumerate(concerned_settings) if group["group"] == g.id),
                    None,
                )
                if group_index is None:
                    continue
                concerned_settings[group_index]["is_forced"].add(-1)
            for g in dossier_settings.tenure_allow_visibility_from.all():
                group_index = next(
                    (i for i, group in enumerate(concerned_settings) if group["group"] == g.id),
                    None,
                )
                if group_index is None:
                    continue
                concerned_settings[group_index]["is_allowed"].add(-1)

            try:
                responsible = ResponsibleModel.objects.get(user=self.request.user)
                if responsible.tenure.filter(id=serializer.instance.student.classe.id).exists():
                    concerned_settings.append(
                        {
                            "group": -1,
                            "is_allowed": set(
                                dossier_settings.tenure_allow_visibility_to.all().values_list(
                                    "id", flat=True
                                )
                            ),
                            "is_forced": set(
                                dossier_settings.tenure_force_visibility_to.all().values_list(
                                    "id", flat=True
                                )
                            ),
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
                    c_s["is_allowed"]
                    .intersection(c_s["is_forced"])
                    .union(c_s["is_forced"].difference(c_s["is_allowed"]))
                )

            only_allowed_perm = set()
            for c_s in concerned_settings:
                only_allowed_perm = only_allowed_perm.union(
                    c_s["is_allowed"].difference(c_s["is_forced"])
                )

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

        return serializer.save(visible_by_groups=visible_by, visible_by_tenure=visible_by_tenure)


class CasEleveViewSet(BaseModelViewSet, ForceVisibilityMixin):
    queryset = CasEleve.objects.filter(student__isnull=False).order_by("-datetime_modified")

    serializer_class = CasEleveSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    filterset_class = CasEleveFilter
    ordering_fields = ("datetime_encodage", "student__last_name", "datetime_modified")
    user_field = "created_by"

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
            filter_by_groups |= Q(student__classe__in=resp.tenure.all(), visible_by_tenure=True)
        except ObjectDoesNotExist:
            pass

        queryset = queryset.filter(filter_by_groups).distinct()
        return queryset

    def perform_create(self, serializer):
        send_to_teachers = serializer.validated_data.get("send_to_teachers", False)
        # Remove from serializer as model doesn't need it.
        if "send_to_teachers" in serializer.validated_data:
            serializer.validated_data.pop("send_to_teachers")

        super().perform_create(serializer)
        cas = serializer.save(created_by=self.request.user)
        if send_to_teachers:
            task_send_info_email.apply_async(
                countdown=1, kwargs={"instance_id": serializer.save().id}
            )

        if cas.sanction_decision:
            if cas.sanction_decision.notify:
                notify_sanction.apply_async(countdown=1, kwargs={"instance_id": cas.id})

        self.force_visibility(serializer)

    def perform_update(self, serializer):
        super().perform_update(serializer)

        if serializer.validated_data["send_to_teachers"]:
            task_send_info_email.apply_async(
                countdown=1, kwargs={"instance_id": serializer.save().id}
            )

        self.force_visibility(serializer)

    def is_only_tenure(self):
        return False


class AskSanctionsView(BaseDossierEleveView):
    template_name = "dossier_eleve/ask_sanctions.html"
    permission_required = ["dossier_eleve.ask_sanction", "dossier_eleve.set_sanction"]
    filters = [
        {"value": "student", "text": "Nom"},
        {"value": "classe", "text": "Classe"},
        {"value": "sanction_decision__sanction_decision", "text": "Sanction/décision"},
        {"value": "date_sanction", "text": "Date sanction"},
        {"value": "datetime_conseil", "text": "Date du conseil"},
        {"value": "datetime_encodage", "text": "Date encodage"},
        {"value": "student__matricule", "text": "Matricule"},
        {"value": "scholar_year", "text": "Année scolaire"},
        {"value": "activate_today", "text": "Sanctions aujourdhui"},
        {"value": "activate_not_done", "text": "Sanctions non faites"},
        {"value": "activate_waiting", "text": "En attente de validation"},
        {"value": "activate_own_classes", "text": "Ses classes"},
    ]

    def has_permission(self) -> bool:
        permissions = self.get_permission_required()
        for p in permissions:
            if self.request.user.has_perm(p):
                return True
        return False


class AskSanctionsFilter(BaseFilters):
    classe = filters.CharFilter(method="classe_by")
    student = filters.CharFilter(method="people_name_by")
    activate_not_done = filters.CharFilter(method="activate_not_done_by")
    activate_waiting = filters.CharFilter(method="activate_waiting_by")
    activate_today = filters.CharFilter(method="activate_today_by")
    sanction_decision = filters.CharFilter(method="sanction_decision_by")

    class Meta:
        fields_to_filter = (
            "student__matricule",
            "sanction_decision__sanction_decision",
            "date_sanction",
            "datetime_conseil",
            "datetime_encodage",
            "sanction_decision__is_retenue",
        )
        model = CasEleve
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def sanction_decision_by(self, queryset, name, value):
        query_filter = Q()
        for i in value.split(","):
            query_filter |= Q(sanction_decision__id=i)
        return queryset.filter(query_filter)

    def activate_not_done_by(self, queryset, name, value):
        if value == "true":
            return queryset.filter(date_sanction__lt=timezone.now())
        return queryset

    def activate_waiting_by(self, queryset, name, value):
        if value == "true":
            return queryset.filter(datetime_conseil__isnull=True, date_sanction__isnull=True)
        return queryset

    def activate_today_by(self, queryset, name, value):
        today = timezone.now()
        if value == "true":
            return queryset.filter(
                date_sanction__day=today.day,
                date_sanction__month=today.month,
                date_sanction__year=today.year,
            )
        return queryset


class AskSanctionsViewSet(ModelViewSet, ForceVisibilityMixin):
    queryset = CasEleve.objects.filter(
        student__isnull=False, sanction_decision__isnull=False, sanction_faite=False
    )
    serializer_class = CasEleveSerializer
    pagination_class = PageNumberSizePagination
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = AskSanctionsFilter
    ordering_fields = (
        "datetime_encodage",
        "date_sanction",
        "student__classe__year",
        "student__classe__letter",
        "student__last_name",
        "sanction_decision__sanction_decision",
    )

    def get_queryset(self):
        sanctions = SanctionDecisionDisciplinaire.objects.filter(can_ask=True)

        queryset = super().get_queryset().filter(sanction_decision__in=sanctions)
        filter_by_groups = Q()
        for g in self.request.user.groups.all():
            filter_by_groups |= Q(visible_by_groups=g)
        filter_by_groups |= Q(created_by=self.request.user)
        # Give access to tenures
        try:
            resp = ResponsibleModel.objects.get(user=self.request.user)
            filter_by_groups |= Q(student__classe__in=resp.tenure.all(), visible_by_tenure=True)
        except ObjectDoesNotExist:
            pass

        queryset = queryset.filter(filter_by_groups).distinct()

        return queryset

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.save(
            sanction_faite=False, user=self.request.user.username, created_by=self.request.user
        )

        cas = self.force_visibility(serializer)

        if cas.sanction_decision:
            if cas.sanction_decision.notify:
                notify_sanction.apply_async(countdown=1, kwargs={"instance_id": cas.id})

    def perform_update(self, serializer):
        super().perform_update(serializer)

        if self.request.method != "PATCH":
            self.force_visibility(serializer)


class InfoViewSet(ReadOnlyModelViewSet):
    queryset = InfoEleve.objects.all()
    serializer_class = InfoEleveSerializer


class SanctionDecisionViewSet(ReadOnlyModelViewSet):
    queryset = SanctionDecisionDisciplinaire.objects.order_by("sanction_decision")
    serializer_class = SanctionDecisionDisciplinaireSerializer

    def get_queryset(self):
        self.queryset = super().get_queryset()
        only_sanctions = self.request.GET.get("only_sanctions", 0) == "1"
        if only_sanctions:
            return self.queryset.filter(can_ask=True)

        return self.queryset


class StatisticAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student, format=None):
        only_sanctions = request.GET.get("only_sanctions", 1) == 1
        only_asked_sanctions = request.GET.get("only_asked_sanctions", 0) == 1
        stats = self.gen_stats(request.user, student, only_sanctions)
        return Response(stats)

    def gen_stats(
        self, user_from, student, only_sanctions=False, only_asked_sanctions=False, all_years=False
    ):
        all_access = get_settings().all_access.all()
        queryset = CasEleve.objects.all()
        if not user_from.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=user_from).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, user_from)
            queryset = queryset.filter(student__classe__in=classes)

        cas_discip = queryset.filter(info=None, student=student).filter(
            Q(sanction_faite=True) | Q(sanction_faite__isnull=True)
        )
        cas_info = queryset.filter(sanction_decision=None, student=student)

        if not all_years:
            current_scolar_year = get_scholar_year()
            limit_date = timezone.make_aware(timezone.datetime(current_scolar_year, 8, 15))
            cas_discip = cas_discip.filter(datetime_encodage__gte=limit_date)
            cas_info = cas_info.filter(datetime_encodage__gte=limit_date)

        sanctions = SanctionStatisticsModel.objects.all()
        infos = InfoStatisticsModel.objects.all()

        if only_asked_sanctions:
            sanctions = sanctions.filter(sanctions_decisions__can_ask=True).distinct()

        stats = []
        for s in sanctions:
            stat = {
                "display": s.display,
                "value": len(cas_discip.filter(sanction_decision__in=s.sanctions_decisions.all())),
                "type": "sanction-decision",
            }
            stats.append(stat)

        for i in infos:
            stat = {
                "display": i.display,
                "value": len(cas_info.filter(info__in=i.info.all())),
                "type": "info",
            }
            stats.append(stat)

        if not only_sanctions:
            stats.append({"display": "Non disciplinaire", "value": len(cas_info), "type": "total"})
            stats.append(
                {"display": "Total disciplinaire", "value": len(cas_discip), "type": "total"}
            )

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
                attachment = CasAttachment.objects.get(
                    attachment__exact=f"dossier_eleve/{year}/{str(month).zfill(2)}/{str(day).zfill(2)}/{file}"
                )
            queryset = CasEleve.objects.filter(attachments=attachment)
            filter_by_groups = Q()
            for g in request.user.groups.all():
                filter_by_groups |= Q(visible_by_groups=g)
            filter_by_groups |= Q(created_by=request.user)
            resp = ResponsibleModel.objects.get(user=request.user)
            filter_by_groups |= Q(student__classe__in=resp.tenure.all(), visible_by_tenure=True)
            queryset = queryset.filter(filter_by_groups).distinct()
            if not queryset.exists():
                return HttpResponse(status=404)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

        response = HttpResponse(attachment.attachment, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{file if file else attachment.attachment.name}"'
        )

        return response


class CasEleveListPDFGen(LoginRequiredMixin, PermissionRequiredMixin, WeasyTemplateView):
    permission_required = ["dossier_eleve.view_caseleve"]
    template_name = "dossier_eleve/cas_list_pdf.html"

    def get_context_data(self, **kwargs) -> dict:
        view_set = CasEleveViewSet.as_view({"get": "list"})
        results = [c["id"] for c in view_set(self.request).data["results"]]
        results = CasEleve.objects.filter(id__in=results)
        context = {"list": results}
        return context

    def modify_entries(self, results):
        return results


class CasElevePDFGenAPI(LoginRequiredMixin, PermissionRequiredMixin, WeasyTemplateView):
    template_name = "dossier_eleve/discip_pdf.html"
    permission_required = ["dossier_eleve.view_caseleve"]

    def get(self, request, *args, **kwargs):
        if request.GET.get("student__matricule"):
            return self.render_to_response(self.generate_context(request))

        elif request.GET.get("classe"):
            classe_access = get_classes(get_settings().teachings.all(), True, request.user)
            try:
                classe = classe_access.get(id=request.GET["classe"])
            except ObjectDoesNotExist:
                return HttpResponse("Vous n'avez pas les accès nécessaire.", status=401)

            students = People().get_students_by_classe(classe)
            merger = PdfWriter()
            added = False
            for s in students:
                request.GET = request.GET.copy()
                request.GET["student__matricule"] = s.matricule
                student_context = self.generate_context(request)
                if not student_context:
                    continue
                student_response = self.render_to_response(student_context)
                pdf = BytesIO(student_response.rendered_content)
                if not pdf:
                    continue

                merger.append(pdf)
                added = True

            if not added:
                return render(request, "dossier_eleve/no_student.html")

            output_stream = BytesIO()
            merger.write(output_stream)
            merger.close()
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'filename; filename="' + classe.compact_str + '.pdf"'
            response.write(output_stream.getvalue())
            return response
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    @staticmethod
    def generate_context(request):
        if request.GET.get("classe"):
            request.GET.pop("classe")
        view_set = CasEleveViewSet.as_view({"get": "list"})
        results = view_set(request).data["results"]
        if not results:
            return None

        # Use datetime object instead of plain text.
        for r in results:
            r["datetime_encodage"] = timezone.datetime.strptime(
                r["datetime_encodage"][:19], "%Y-%m-%dT%H:%M:%S"
            )
            if r["info"]:
                continue
            r["date_sanction"] = (
                timezone.datetime.strptime(r["date_sanction"][:19], "%Y-%m-%d")
                if r["date_sanction"]
                else None
            )
        student = StudentModel.objects.get(matricule=request.GET["student__matricule"])
        check_student_photo(student)

        all_years = not request.GET.get("scholar_year", False)
        context = {
            "statistics": StatisticAPI().gen_stats(request.user, student, all_years=all_years)
        }
        tenure = ResponsibleModel.objects.filter(tenure=student.classe).first()
        context["tenure"] = tenure.fullname if tenure else "—"

        context["student"] = student
        context["list"] = results
        return context


class AskSanctionBasePDF(WeasyTemplateView):
    field_date = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        view_set = AskSanctionsViewSet.as_view({"get": "list"})
        results = view_set(self.request).data["results"]
        results = self.modify_entries(results)

        date_from = self.request.GET.get("%s__gte" % self.field_date)[:10]
        date_to = self.request.GET.get("%s__lte" % self.field_date)[:10]
        context = {"date_from": date_from, "date_to": date_to, "list": results}
        return context

    def modify_entries(self, results):
        for r in results:
            if r["date_sanction"]:
                r["date_sanction"] = timezone.datetime.strptime(r["date_sanction"][:19], "%Y-%m-%d")
            else:
                r["date_sanction"] = None
            if r["datetime_conseil"]:
                r["datetime_conseil"] = timezone.datetime.strptime(
                    r["datetime_conseil"][:19], "%Y-%m-%dT%H:%M:%S"
                )
            r["demandeur"] = r["demandeur"].split(" — ")[0]
        return results


class AskSanctionCouncilPDF(AskSanctionBasePDF):
    template_name = "dossier_eleve/discip_council_pdf.html"
    field_date = "datetime_conseil"


class AskSanctionRetenuesPDF(AskSanctionBasePDF):
    template_name = "dossier_eleve/discip_retenues_pdf.html"
    field_date = "date_sanction"


class SanctionPDF(APIView):
    permission_required = ["dossier_eleve.ask_sanction", "dossier_eleve.view_caseleve"]
    renderer_classes = [BinaryFileRenderer]

    def post(self, request, format=None):
        template = get_template("dossier_eleve/sanction_pdf.html")
        context = {
            "sanction": CasEleve.objects.get(id=request.data.get("sanction")),
            "text": request.data.get("text"),
            "core_settings": get_core_settings(),
        }
        html_render = template.render(context)
        pdf_file = HTML(string=html_render).write_pdf()
        return Response(
            pdf_file,
            headers={"Content-Disposition": 'attachment; filename="file.pdf"'},
            content_type="application/pdf",
        )


class SanctionTemplate(
    APIView,
):
    permission_required = [
        "dossier_eleve.ask_sanction",
        "dossier_eleve.view_caseleve",
        "dossier_eleve.add_caseleve",
    ]

    def get(self, request, cas_id, format=None):
        try:
            cas = CasEleve.objects.get(id=cas_id)
        except ObjectDoesNotExist:
            return Response(None)

        template = cas.sanction_decision.letter_comment
        t = Template(template)
        core_settings = get_core_settings()
        c = Context({"sanction": cas, "core_settings": core_settings})
        return Response(t.render(context=c))


class WarnSanctionAPI(APIView):
    permission_required = [
        "dossier_eleve.ask_sanction",
        "dossier_eleve.view_caseleve",
        "dossier_eleve.add_caseleve",
    ]

    def post(self, request, format=None):
        sanction = CasEleve.objects.get(id=request.data.get("cas_id"))
        recipients = request.data.get("recipients")
        reply_to = request.data.get("reply_to", [])
        context = {
            "sanction": sanction,
            "text": request.data.get("msg"),
            "core_settings": get_core_settings(),
        }

        resp_school = get_resp_emails(sanction.student)

        # Get recipients.
        recipient_email = set()
        if "mother" in recipients:
            recipient_email.add(sanction.student.additionalstudentinfo.mother_email)
        if "father" in recipients:
            recipient_email.add(sanction.student.additionalstudentinfo.father_email)
        if "student" in recipients:
            recipient_email.add(sanction.student.additionalstudentinfo.student_email)
        if "resp" in recipients:
            recipient_email.add(sanction.student.additionalstudentinfo.resp_email)
        if "resp_school" in recipients:
            recipient_email = recipient_email.union(resp_school)

        other_responsibles = ResponsibleModel.objects.filter(
            pk__in=request.data.get("other_recipients")
        )
        recipient_email = recipient_email.union(
            {
                r.email_school if get_settings().use_school_email else r.email
                for r in other_responsibles
            }
        )

        for r in recipient_email:
            send_email(
                [r],
                subject=f"Sanction concernant {sanction.student.fullname}",
                email_template="dossier_eleve/email_sanction_parents.html",
                context=context,
                reply_to=reply_to,
            )
        sanction.notified = True
        sanction.save()

        # Log notification
        log = NotificationLogModel(
            application="dossier_eleve",
            related_view="WarnSanctionAPI",
            related_object=sanction.pk,
            student=sanction.student,
            message=request.data.get("msg"),
            recipients=list(recipient_email),
            author=request.user,
            status=NotificationLogModel.DONE,
        )
        log.save()

        return Response(status=201)


if "proeco" in settings.INSTALLED_APPS:
    from proeco.views import ExportStudentSelectionAPI

    class ExportStudentToProEco(ExportStudentSelectionAPI):
        def _get_student_list(self, request, kwargs, own_classes="false"):
            date_from = kwargs["date_from"]
            date_to = kwargs["date_to"]
            export_type = kwargs["export_type"]
            sanctions = kwargs["sanctions"].split(",")
            own_classes = (
                kwargs["own_classes"] if "own_classes" in kwargs else own_classes
            ) == "true"

            sanctions = CasEleve.objects.filter(
                student__isnull=False,
                sanction_decision__in=sanctions,
                sanction_faite=False,
            )

            if own_classes:
                classes = get_classes(
                    teaching=get_settings().teachings.all(),
                    check_access=True,
                    user=self.request.user,
                    tenure_class_only=False,
                    educ_by_years=False,
                )
                sanctions.filter(student__classe__in=list(classes))

            if export_type == "council":
                sanctions = sanctions.filter(
                    datetime_conseil__gte=date_from,
                    datetime_conseil__lte=date_to,
                )
            elif export_type == "retenue":
                sanctions = sanctions.filter(
                    date_sanction__gte=date_from,
                    date_sanction__lte=date_to,
                )

            return sanctions.values_list("student", flat=True)

        def _format_file_name(self, request, **kwargs):
            return f"Pref_NOMS_{timezone.now().strftime('%y-%m-%d')}_sanctions.TXT"
