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
import datetime

from escpos.printer import Network, Dummy
from unidecode import unidecode

from weasyprint import HTML

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.contrib.auth.models import Group
from django.db.models import ObjectDoesNotExist, Count, Q
from django.utils import timezone
from django.conf import settings
from django.template import Template, Context

from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import ResponsibleModel, TeachingModel, StudentModel, NotificationLogModel
from core.utilities import get_menu
from core.views import BaseModelViewSet, BaseFilters, BinaryFileRenderer, get_core_settings
from core.email import get_resp_emails, send_email
from core.people import get_classes
from core.serializers import StudentSerializer

from .models import LatenessSettingsModel, LatenessModel, SanctionTriggerModel, MailTemplateModel
from .serializers import (
    LatenessSettingsSerializer,
    LatenessSerializer,
    MailTemplateSerializer,
)


def get_menu_entry(active_app, request):
    if not request.user.has_perm("lateness.view_latenessmodel"):
        return {}
    return {
        "app": "lateness",
        "display": "Retards",
        "url": "/lateness/",
        "active": active_app == "lateness",
    }


def get_settings():
    settings_lateness = LatenessSettingsModel.objects.first()
    if not settings_lateness:
        # Create default settings.
        settings_lateness = LatenessSettingsModel.objects.create()
        if TeachingModel.objects.count() == 1:
            settings_lateness.teachings.add(TeachingModel.objects.first())
        settings_lateness.save()

    return settings_lateness


class LatenessView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "lateness/lateness.html"
    permission_required = "lateness.view_latenessmodel"
    filters = [
        {"value": "student", "text": "Nom"},
        {"value": "student__matricule", "text": "Matricule"},
        {"value": "date_lateness", "text": "Date"},
        {"value": "classe", "text": "Classe"},
        {"value": "count_lateness", "text": "Nombre de retard"},
        {"value": "activate_after_count", "text": "À partir du comptage"},
        {"value": "activate_own_classes", "text": "Ses classes"},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["menu"] = json.dumps(get_menu(self.request, "lateness"))
        context["filters"] = json.dumps(self.filters)
        context["settings"] = json.dumps((LatenessSettingsSerializer(get_settings()).data))
        context["hasSettingsPerm"] = json.dumps(
            self.request.user.has_perm("lateness.view_latenesssettingsmodel")
        )

        return context


class LatenessSettingsViewSet(GenericViewSet, UpdateModelMixin):
    queryset = LatenessSettingsModel.objects.all()
    serializer_class = LatenessSettingsSerializer
    permission_classes = [DjangoModelPermissions]


class LatenessFilter(BaseFilters):
    datetime_field = "datetime_creation"

    student = filters.CharFilter(method="people_name_by")
    date_lateness__gte = filters.DateFilter(method="date_lateness_by")
    date_lateness__lte = filters.DateFilter(method="date_lateness_by")
    count_lateness = filters.NumberFilter(method="count_lateness_by")
    activate_after_count = filters.BooleanFilter(method="activate_after_count_by")
    classe = filters.CharFilter(method="classe_by")

    class Meta:
        fields_to_filter = [
            "student__matricule",
        ]
        model = LatenessModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def count_lateness_by(self, queryset, field_name, value):
        date_from = get_settings().date_count_start
        counting = (
            LatenessModel.objects.filter(justified=False, datetime_creation__gte=date_from)
            .values("student")
            .annotate(count_lateness=Count("student"))
            .filter(count_lateness__gte=value)
            .values_list("student", flat=True)
        )
        return LatenessModel.objects.filter(student__in=counting, justified=False)

    def date_lateness_by(self, queryset, field_name, value):
        if "gte" in field_name:
            return queryset.filter(datetime_creation__gte=value)
        else:
            midnight = datetime.datetime.combine(value, datetime.datetime.max.time())
            return queryset.filter(datetime_creation__lte=midnight)

    def activate_after_count_by(self, queryset, field_name, value):
        return queryset.filter(datetime_creation__gte=get_settings().date_count_start)


class LatenessViewSet(BaseModelViewSet):
    queryset = LatenessModel.objects.all()
    serializer_class = LatenessSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    ordering_fields = (
        "datetime_update",
        "datetime_creation",
    )
    filterset_class = LatenessFilter
    username_field = None

    if "student_absence_teacher" in settings.INSTALLED_APPS:

        def _get_student_absence_teacher(self, instance, time):
            from student_absence_teacher.models import StudentAbsenceTeacherModel, PeriodModel

            try:
                period = PeriodModel.objects.get(start__lt=time, end__gte=time)
            except ObjectDoesNotExist:
                return

            try:
                return StudentAbsenceTeacherModel.objects.get(
                    date_absence=instance.datetime_creation,
                    student=instance.student,
                    period=period,
                )
            except ObjectDoesNotExist:
                return None

        def _update_student_absence_teacher(self, instance, time):
            from student_absence_teacher.models import StudentAbsenceTeacherModel, PeriodModel

            student_lateness = self._get_student_absence_teacher(instance, time)
            if not student_lateness:
                try:
                    period = PeriodModel.objects.get(start__lt=time, end__gte=time)
                except ObjectDoesNotExist:
                    return

                student_lateness = StudentAbsenceTeacherModel(
                    date_absence=instance.datetime_creation,
                    student=instance.student,
                    period=period,
                    status=StudentAbsenceTeacherModel.LATENESS,
                    user=self.request.user,
                )
            student_lateness.comment = f"Retard à {time.time().strftime('%H:%M')} {'(justifié)' if instance.justified else ''}"
            student_lateness.user = self.request.user
            student_lateness.save()

        def _remove_student_absence_teacher(self, instance):
            from student_absence_teacher.models import StudentAbsenceTeacherModel

            student_lateness = self._get_student_absence_teacher(
                instance, instance.datetime_update.astimezone().time()
            )
            if student_lateness:
                student_lateness.delete()

    def perform_create(self, serializer):
        lateness = serializer.save()
        printing = self.request.query_params.get("print", None)
        printer = self.request.query_params.get("printer", 0)

        lateness_settings = get_settings()

        lateness_count = (
            self.get_queryset()
            .filter(
                datetime_creation__gte=get_settings().date_count_start,
                student=lateness.student,
                justified=False,
            )
            .count()
        )

        if lateness_settings.printer and printing:
            try:
                if settings.DEBUG:
                    print(printer)
                printer = Network(printer) if not settings.DEBUG else Dummy()
                printer.charcode()
                printer.set(align="center", bold=True)
                printer.text("RETARD\n")
                printer.set(align="left")
                absence_dt = lateness.datetime_creation.astimezone(timezone.get_default_timezone())

                count_or_justified = (
                    "Retard justifié" if lateness.justified else "Nombre de retards: "
                )
                if not lateness.justified:
                    count_or_justified += "%i" % lateness_count

                printer.text(
                    "\n%s %s\n%s\n%s\n%s\nBonne journée !"
                    % (
                        unidecode(lateness.student.last_name),
                        unidecode(lateness.student.first_name),
                        lateness.student.classe.compact_str,
                        absence_dt.strftime("%H:%M - %d/%m/%Y"),
                        count_or_justified,
                    )
                )
                if settings.DEBUG:
                    print(printer.output)
                printer.cut()
                printer.close()
            except OSError:
                pass

        now = timezone.localtime()

        # Trigger
        sanction_next = False
        if not lateness.justified:
            for trigger in (
                SanctionTriggerModel.objects.filter(teaching=lateness.student.teaching)
                .filter(
                    Q(year__year=lateness.student.classe.year) | Q(classe=lateness.student.classe)
                )
                .filter(
                    Q(
                        time_lateness_start__isnull=False,
                        time_lateness_stop__isnull=False,
                        time_lateness_start__lte=now,
                        time_lateness_stop__gt=now,
                    )
                    | Q(
                        time_lateness_start__isnull=True,
                        time_lateness_stop__isnull=True,
                    )
                )
                .distinct()
            ):

                count_first = trigger.lateness_count_trigger_first
                count_trigger = trigger.lateness_count_trigger

                # Check if trigger will be hit next time.
                if lateness_count + 1 == count_first or (
                    lateness_count >= count_first
                    and (lateness_count + 1 - count_first) % count_trigger == 0
                ):
                    sanction_next = True

                # Check if it is triggered.
                if lateness_count < count_first or (
                    lateness_count > count_first
                    and (lateness_count - count_first) % count_trigger != 0
                ):
                    continue

                lateness.has_sanction = True
                if trigger.only_warn:
                    lateness.save()
                    continue
                from dossier_eleve.models import CasEleve, SanctionDecisionDisciplinaire

                sanction = SanctionDecisionDisciplinaire.objects.get(id=trigger.sanction_id)
                today = datetime.datetime.today()
                # next_week_day == 7 is the same day
                if trigger.next_week_day < 7:
                    day_shift = 6 + trigger.next_week_day
                    day = today + datetime.timedelta(
                        days=(day_shift - today.isoweekday()) % (6 + trigger.delay) + 1
                    )
                else:
                    day = today
                day = day.replace(
                    hour=trigger.sanction_time.hour, minute=trigger.sanction_time.minute
                )

                cas = CasEleve.objects.create(
                    student=lateness.student,
                    name=lateness.student.display,
                    demandeur=self.request.user.get_full_name(),
                    sanction_decision=sanction,
                    explication_commentaire="Sanction pour cause de retard.",
                    sanction_faite=False,
                    date_sanction=day,
                    created_by=self.request.user,
                )
                cas.visible_by_groups.set(Group.objects.all())
                lateness.sanction_id = cas.id
                lateness.save()

        # Notification
        if lateness_settings.notify_responsible:
            responsibles = get_resp_emails(lateness.student)

            context = {
                "lateness": lateness,
                "lateness_count": lateness_count,
                "warning": sanction_next,
                "core_settings": get_core_settings(),
            }
            send_email(
                responsibles,
                "[Retard]%s  %s %s"
                % (
                    "[Sanction]" if lateness.has_sanction else "",
                    lateness.student.fullname,
                    lateness.student.classe.compact_str,
                ),
                "lateness/lateness_email.html",
                context=context,
            )

        # Student absence teacher.
        if "student_absence_teacher" in settings.INSTALLED_APPS:
            self._update_student_absence_teacher(lateness, now)

    def remove_sanction(self, instance):
        if instance.sanction_id:
            from dossier_eleve.models import CasEleve

            try:
                CasEleve.objects.get(id=instance.sanction_id).delete()
            except ObjectDoesNotExist:
                pass
            instance.sanction_id = None
            instance.save()

    def perform_destroy(self, instance):
        self.remove_sanction(instance)
        self._remove_student_absence_teacher(instance)
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.sanction_id and instance.justified:
            self.remove_sanction(instance)

        # Student absence teacher.
        if "student_absence_teacher" in settings.INSTALLED_APPS:
            # Take update time to show in student_absence_teacher comment
            self._update_student_absence_teacher(instance, timezone.localtime())

    def get_group_all_access(self):
        return get_settings().all_access.all()


if "proeco" in settings.INSTALLED_APPS:
    from proeco.views import ExportStudentSelectionAPI

    class ExportStudentToProEco(ExportStudentSelectionAPI):
        def _get_student_list(self, request, kwargs):
            part_of_day = kwargs["part_of_day"]
            today = timezone.now()
            today_lateness = LatenessModel.objects.filter(
                datetime_creation__year=today.year,
                datetime_creation__month=today.month,
                datetime_creation__day=today.day,
                justified=False,
            )
            noon = timezone.make_aware(
                datetime.datetime(today.year, today.month, today.day, hour=12)
            )
            if part_of_day == "AM":
                today_lateness = today_lateness.filter(datetime_creation__lte=noon)
            elif part_of_day == "PM":
                today_lateness = today_lateness.filter(datetime_creation__gt=noon)

            return today_lateness.values_list("student", flat=True)

        def _format_file_name(self, request, **kwargs):
            return f"Pref_NOMS_{timezone.now().strftime('%y-%m-%d')}_retards.TXT"


class TopLatenessAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not request.user.has_perm("lateness.view_latenessmodel"):
            return Response([])

        date_from = get_settings().date_count_start
        latenesses = LatenessModel.objects.filter(justified=False, datetime_creation__gte=date_from)

        own_classes = request.GET.get("own_classes", False)
        if own_classes:
            classes = get_classes(
                check_access=True,
                user=self.request.user,
                tenure_class_only=True,
                educ_by_years="both",
            ).values_list("id")
            latenesses = latenesses.filter(student__classe__id__in=classes)
        top_list = (
            latenesses.values("student")
            .annotate(count_lateness=Count("student"))
            .order_by("-count_lateness")
            .values_list("student", "count_lateness")[:50]
        )

        top_list = [
            {
                "student": StudentSerializer(StudentModel.objects.get(matricule=s[0])).data,
                "count": s[1],
            }
            for s in top_list
        ]

        return Response(top_list)


class MailTemplateViewSet(ReadOnlyModelViewSet):
    queryset = MailTemplateModel.objects.all()
    serializer_class = MailTemplateSerializer
    permission_required = [
        "lateness.add_latenessmodel",
    ]

    def retrieve(self, request, pk=None):
        student = request.query_params.get("student")

        try:
            student = StudentModel.objects.get(matricule=student)
        except ObjectDoesNotExist:
            return Response(None)

        template = MailTemplateModel.objects.get(pk=pk)
        t = Template(template.template)

        last_latenesses = LatenessModel.objects.filter(
            student=student,
            datetime_creation__gte=get_settings().date_count_start,
        ).order_by("datetime_creation")

        c = Context({"student": student, "last_latenesses": last_latenesses})
        return Response(t.render(context=c))


class WarningPDF(APIView):
    permission_required = [
        "lateness.add_latenessmodel",
    ]
    renderer_classes = [BinaryFileRenderer]

    def post(self, request, format=None):
        template = get_template("lateness/warning_pdf.html")
        context = {
            "student": StudentModel.objects.get(matricule=request.data.get("student_id")),
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


class MailWarningAPI(APIView):
    permission_required = [
        "lateness.add_latenessmodel",
    ]

    def post(self, request, format=None):
        try:
            student = StudentModel.objects.get(matricule=request.data.get("student_id", 0))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        recipients = request.data.get("recipients", [])
        context = {
            "student": student,
            "text": request.data.get("msg"),
            "core_settings": get_core_settings(),
            "last_latenesses": LatenessModel.objects.filter(
                student__matricule=request.data.get("student_id"),
                datetime_creation__gte=get_settings().date_count_start,
            ),
        }

        resp_school = get_resp_emails(student)

        # Get recipients.
        recipient_email = set()
        if "mother" in recipients:
            recipient_email.add(student.additionalstudentinfo.mother_email)
        if "father" in recipients:
            recipient_email.add(student.additionalstudentinfo.father_email)
        if "resp" in recipients:
            recipient_email.add(student.additionalstudentinfo.resp_email)
        if "resp_school" in recipients:
            recipient_email = recipient_email.union(resp_school)

        other_responsibles = ResponsibleModel.objects.filter(
            pk__in=request.data.get("other_recipients")
        )
        recipient_email = recipient_email.union(
            {
                r.email_school if r.email_school else r.email
                for r in other_responsibles
                if r.email_school or r.email
            }
        )

        for r in recipient_email:
            send_email(
                [r],
                subject=f"Arrivées tardives concernant {student.fullname}",
                email_template="lateness/email_warning_parents.html",
                context=context,
                reply_to=list(resp_school),
            )

        # Log notification
        log = NotificationLogModel(
            application="lateness",
            related_view="MailWarningAPI",
            student=student,
            message=request.data.get("msg"),
            recipients=list(recipient_email),
            author=request.user,
            status=NotificationLogModel.DONE,
        )
        log.save()

        return Response(status=201)
