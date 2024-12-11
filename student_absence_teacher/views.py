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

import csv
import json
import datetime
from itertools import groupby

from weasyprint import HTML
from escpos.printer import Network

from django_weasyprint import WeasyTemplateView

from django.template.loader import get_template
from django.template import Template, Context
from django.db.models import Count, ObjectDoesNotExist, Q
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone

from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework import status

from core.models import ClasseModel, StudentModel, ResponsibleModel
from core.utilities import get_menu, get_scholar_year
from core.people import get_classes
from core.email import send_email, get_resp_emails
from core.views import (
    BaseFilters,
    PageNumberSizePagination,
    DjangoModelWithAccessPermissions,
    get_core_settings,
    LargePageSizePagination,
    BinaryFileRenderer,
)

from .models import (
    StudentAbsenceTeacherSettingsModel,
    StudentAbsenceTeacherModel,
    StudentAbsenceEducModel,
    PeriodModel,
    PeriodEducModel,
    JustificationModel,
    JustMotiveModel,
    MailTemplateModel,
)
from .serializers import (
    StudentAbsenceTeacherSettingsSerializer,
    StudentAbsenceEducSerializer,
    PeriodTeacherSerializer,
    PeriodEducSerializer,
    StudentAbsenceTeacherSerializer,
    JustificationSerializer,
    JustMotiveSerializer,
)


def get_menu_entry(active_app: str, request) -> dict:
    if not request.user.has_perm("student_absence_teacher.view_studentabsenceteachermodel"):
        return {}
    return {
        "app": "student_absence_teacher",
        "display": "Abs. Élèves",
        "url": "/student_absence_teacher",
        "active": active_app == "student_absence_teacher",
    }


def get_settings():
    settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.first()
    if not settings_student_absence:
        # Create default settings.
        settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.create().save()

    return settings_student_absence


class StudentAbsenceTeacherView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "student_absence_teacher/student_absence_teacher.html"
    permission_required = "student_absence_teacher.view_studentabsenceteachermodel"
    filters = [
        {"value": "student__display", "text": "Nom"},
        {"value": "student__matricule", "text": "Matricule"},
        {"value": "classe", "text": "Classe"},
        {"value": "period__name", "text": "Période"},
        {"value": "activate_absent", "text": "Absents"},
        {"value": "date_absence", "text": "Date"},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["menu"] = json.dumps(get_menu(self.request, "student_absence_absence"))
        context["filters"] = json.dumps(self.filters)
        context["settings"] = json.dumps(
            (StudentAbsenceTeacherSettingsSerializer(get_settings()).data)
        )
        context["proeco"] = json.dumps("proeco" in settings.INSTALLED_APPS)

        return context


class StudentAbsenceTeacherFilter(BaseFilters):
    student__display = filters.CharFilter(method="people_name_by")
    classe = filters.CharFilter(method="classe_by")
    activate_absent = filters.BooleanFilter(method="activate_absent_by")

    class Meta:
        fields_to_filter = [
            "student",
            "date_absence",
            "student__matricule",
            "student__classe",
            "period",
            "period__name",
            "datetime_update",
            "status",
        ]
        model = StudentAbsenceTeacherModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, field_name, value):
        if not value[0].isdigit():
            return queryset

        if len(value) > 0:
            queryset = queryset.filter(student__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(student__classe__letter__istartswith=value[1:])
        return queryset

    def activate_absent_by(self, queryset, field_name, value):
        return queryset.filter(status=StudentAbsenceTeacherModel.ABSENCE)


class StudentAbsenceTeacherViewSet(ModelViewSet):
    queryset = StudentAbsenceTeacherModel.objects.filter(student__isnull=False)
    serializer_class = StudentAbsenceTeacherSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = StudentAbsenceTeacherFilter
    ordering_fields = [
        "date_absence",
        "datetime_update",
        "datetime_creation",
        "period",
    ]
    pagination_class = PageNumberSizePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentAbsenceEducFilter(BaseFilters):
    datetime_field = "date_absence"

    student__display = filters.CharFilter(method="people_name_by")
    classe = filters.CharFilter(method="classe_by")
    activate_last_absence = filters.BooleanFilter(method="activate_last_absence_by")
    activate_today_absence = filters.BooleanFilter(method="activate_today_absence_by")
    activate_own_classes = filters.BooleanFilter(method="activate_own_classes_by")
    activate_no_justification = filters.BooleanFilter(method="activate_no_justification_by")

    class Meta:
        fields_to_filter = [
            "student",
            "date_absence",
            "student__matricule",
            "status",
            "student__classe",
            "period__name",
            "mail_warning",
        ]
        model = StudentAbsenceEducModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        fields["period__start"] = ["lt", "gt", "lte", "gte", "exact"]
        fields["period__end"] = ["lt", "gt", "lte", "gte", "exact"]
        filter_overrides = BaseFilters.Meta.filter_overrides

    def activate_last_absence_by(self, queryset, name, value):
        current_date = timezone.now().date()
        return queryset.filter(
            user=self.request.user,
            date_absence=current_date,
            status=StudentAbsenceEducModel.ABSENCE,
        )

    def activate_today_absence_by(self, queryset, name, value):
        current_date = timezone.now().date()
        return queryset.filter(
            date_absence=current_date, status=StudentAbsenceEducModel.ABSENCE
        ).distinct("student")

    def activate_own_classes_by(self, queryset, name, value):
        if not value:
            return queryset

        classes = get_classes(
            check_access=True,
            user=self.request.user,
        )
        return queryset.filter(student__classe__in=classes)

    def activate_no_justification_by(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(justificationmodel__isnull=True)


class ExcludeStudentAPI(APIView):

    def post(self, request, format=None):
        student_id = request.data.get("student_id", None)
        try:
            student = StudentModel.objects.get(matricule=student_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        period_id = request.data.get("period_id", None)
        try:
            period = PeriodModel.objects.get(id=period_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check permission.
        app_settings = get_settings()
        if (
            not self.request.user.groups.all()
            .intersection(app_settings.can_see_exclusion.all())
            .exists()
        ):
            return Response(status=status.HTTP_404_NOT_FOUND)

        today = timezone.now()

        exclusion = StudentAbsenceTeacherModel(
            student=student,
            date_absence=today,
            status=StudentAbsenceTeacherModel.EXCLUDED,
            period=period,
            user=request.user,
        )
        exclusion.save()

        if "lateness" in settings.INSTALLED_APPS:
            from lateness.models import LatenessSettingsModel

            try:
                printer_ip = LatenessSettingsModel.objects.first().printer
                printer = Network(printer_ip)
                printer.charcode("AUTO")
                printer.set(align="center")
                printer.text("EXCLUSION\n")
                printer.set(align="left")
                printer.text(f" {student.fullname_classe}\n")
                printer.text(f" Exclusion de la periode :\n")
                printer.text(f" {period.display}\n\n")
                printer.cut()
                printer.close()
            except OSError:
                pass

        return Response(status=status.HTTP_201_CREATED)


class StudentAbsenceEducViewSet(ModelViewSet):
    queryset = StudentAbsenceEducModel.objects.all()
    serializer_class = StudentAbsenceEducSerializer
    permission_classes = [DjangoModelWithAccessPermissions]
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = StudentAbsenceEducFilter
    pagination_class = PageNumberSizePagination
    ordering_fields = [
        "date_absence",
        "datetime_update",
        "datetime_creation",
        "student__classe__year",
        "student__classe__letter",
        "student__last_name",
        "student__first_name",
        "period__start",
    ]
    cursor = None
    fdb_server = None

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list) and len(request.data) == 0:
            return Response(status=status.HTTP_201_CREATED)

        if get_settings().sync_with_proeco:
            from libreschoolfdb import absences

            first_absence = request.data[0] if isinstance(request.data, list) else request.data
            teaching_name = StudentModel.objects.get(
                matricule=first_absence.get("student_id")
            ).teaching.name

            server = [
                s["server"] for s in settings.SYNC_FDB_SERVER if s["teaching_name"] == teaching_name
            ]
            if len(server) == 0:
                raise

            self.fdb_server = server[0]
            self.cursor = absences._get_absence_cursor(fdb_server=self.fdb_server)

        # if isinstance(request.data, list) and len(request.data) > 0:
        absences_done = []
        for absence in request.data:
            serializer = self.get_serializer(data=absence)
            serializer.is_valid(raise_exception=True)
            if get_settings().sync_with_proeco:
                if not self.sync_proeco(serializer.validated_data):
                    continue

            # Save object and add user/username.
            abs_object = serializer.save()
            abs_object.user = request.user
            abs_object.save()

            absences_done.append(serializer.data)
        if get_settings().sync_with_proeco:
            self.cursor.connection.commit()
            self.cursor.connection.close()
        return Response(absences_done, status=status.HTTP_201_CREATED)

    def sync_proeco(self, data: dict):
        from libreschoolfdb import writer

        if self.cursor:
            periods = PeriodEducModel.objects.all().order_by("start")
            period = [i for i, p in enumerate(periods) if p.id == data.get("period", None).id][0]

            return writer.set_student_absence(
                matricule=data.get("student").matricule,
                day=data.get("date_absence"),
                period=period,
                absence_status=data.get("status"),
                cur=self.cursor,
                fdb_server=self.fdb_server,
                commit=False,
            )
        return False


class PeriodTeacherViewSet(ReadOnlyModelViewSet):
    queryset = PeriodModel.objects.all().order_by("start")
    serializer_class = PeriodTeacherSerializer


class PeriodEducFilter(BaseFilters):
    class Meta:
        model = PeriodEducModel
        fields = {
            "start": ["lt", "gt", "lte", "gte", "exact"],
            "end": ["lt", "gt", "lte", "gte", "exact"],
        }
        filter_overrides = BaseFilters.Meta.filter_overrides


class PeriodEducViewSet(ReadOnlyModelViewSet):
    queryset = PeriodEducModel.objects.all()
    serializer_class = PeriodEducSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PeriodEducFilter


class OverviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def _extract_count_from_educator(self, classe, absences, periods, date):
        counts = {"classe": classe.compact_str, "classe__id": classe.id}

        teacher_abs = StudentAbsenceTeacherModel.objects.filter(
            student__classe=classe,
            date_absence=date,
        )
        for period in periods:
            teacher_abs_period = teacher_abs.filter(
                period__start__lt=period.end, period__end__gt=period.start
            )
            # If teacher count is -1, it means that the teacher didn't take attendences.
            if teacher_abs_period.count() > 0:
                teacher_count = (
                    teacher_abs_period.filter(status=StudentAbsenceTeacherModel.ABSENCE)
                    .distinct("student")
                    .count()
                )
            else:
                teacher_count = -1
            counts[f"period-{period.id}"] = {"teacher_count": teacher_count}
            # Hu?
            counts[f"period-{period.id}"]["not_teacher_count"] = next(
                (x["id__count"] for x in absences if x["period"] == period.id and x["is_absent"]),
                next((0 for y in absences if y["period"] == period.id), -1),
            )
        return counts

    def _extract_count_from_teacher(self, classe, absences, periods, date):
        counts = {"classe": classe.compact_str, "classe__id": classe.id}

        teacher_attendance = StudentAbsenceTeacherModel.objects.filter(
            date_absence=date, student__classe=classe
        )
        educ_attendance_day = StudentAbsenceEducModel.objects.filter(
            date_absence=date, student__classe=classe
        )

        for period in PeriodModel.objects.all():
            educ_attendance_period = educ_attendance_day.filter(
                period__start__lt=period.end, period__end__gt=period.start
            )

            # -1 count means no attendance have been taken.
            teacher_count = (
                -1
                if not teacher_attendance.filter(
                    Q(status=StudentAbsenceTeacherModel.ABSENCE)
                    | Q(status=StudentAbsenceTeacherModel.PRESENCE)
                ).exists()
                else teacher_attendance.filter(
                    period=period, status=StudentAbsenceTeacherModel.ABSENCE
                ).count()
            )

            educ_count = (
                -1
                if not educ_attendance_period.exists()
                else educ_attendance_period.filter(status=StudentAbsenceEducModel.ABSENCE).count()
            )
            counts[f"period-{period.id}"] = {
                "not_teacher_count": educ_count,
                "teacher_count": teacher_count,
            }

        return counts

    def get(self, request, date, point_of_view, class_list="allclass", format=None):
        date = datetime.date.fromisoformat(date)
        classes = ClasseModel.objects.order_by("year", "letter").filter(
            teaching__in=get_settings().teachings.all()
        )
        if class_list == "ownclass":
            classes = get_classes(
                teaching=get_settings().teachings.all(),
                check_access=True,
                user=request.user,
                tenure_class_only=False,
                educ_by_years="both",
            ).order_by("year", "letter")

        if point_of_view == "teacher":
            periods = PeriodModel.objects.order_by("start")
            count_by_classe_by_period = [
                self._extract_count_from_teacher(
                    c,
                    StudentAbsenceTeacherModel.objects.exclude(  ## Exclude only LATENESS ????
                        status=StudentAbsenceTeacherModel.LATENESS
                    )
                    .filter(date_absence=date, student__classe=c)
                    .values("period", "status")
                    .annotate(Count("id")),
                    periods,
                    date,
                )
                for c in classes
            ]

            return Response(json.dumps(count_by_classe_by_period))
        elif point_of_view == "educator":

            periods = PeriodEducModel.objects.order_by("start")
            count_by_classe_by_period = [
                self._extract_count_from_educator(
                    c,
                    StudentAbsenceEducModel.objects.filter(date_absence=date, student__classe=c)
                    .values("period", "status")
                    .annotate(Count("id")),
                    periods,
                    date,
                )
                for c in classes
            ]

            return Response(json.dumps(count_by_classe_by_period))


class ExportAbsencesAPI(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = [
        "student_absence_teacher.view_studentabsenceteachermodel",
    ]

    def _status_by_day(self, statuses: list) -> list:
        status = {s[0]: s[1] for s in StudentAbsenceTeacherModel.STATUS_CHOICES}

        days = [""] * 5
        for s in statuses:
            day = s[4].weekday()
            if day > 5:
                continue
            if days[day]:
                days[day] += f"/{status[s[5]][0].upper()}"
            else:
                days[day] = status[s[5]][0].upper()
        return days

    def get(self, request, document="pdf", date_from=None, date_to=None, format=None):
        absences = StudentAbsenceTeacherModel.objects.filter(
            date_absence__gte=date_from,
            date_absence__lte=date_to,
            student__classe__isnull=False,
        ).exclude(status=StudentAbsenceTeacherModel.PRESENCE)

        # If user cannot see list (overview), only show own absences.
        if (
            not get_settings()
            .can_see_list.filter(id__in=[g.id for g in request.user.groups.all()])
            .exists()
        ):
            absences = absences.filter(user=request.user)
        else:
            classes = get_classes(
                check_access=True, user=request.user, tenure_class_only=False, educ_by_years="both"
            ).values_list("id")
            absences = absences.filter(student__classe__id__in=classes)

        absences = absences.order_by(
            "date_absence", "student__classe__year", "student__classe__letter", "student__last_name"
        )

        if document == "csv":
            absences_list = absences.values_list(
                "student__matricule",
                "student__last_name",
                "student__first_name",
                "student__classe__year",
                "student__classe__letter",
                "student__additionalstudentinfo__group",
                "date_absence",
                "status",
                "period__name",
                "comment",
            )

            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="export.csv"'
            writer = csv.writer(response)
            writer.writerow(
                [
                    "Matricule unique",
                    "Nom",
                    "Prénom",
                    "Année",
                    "Classe",
                    "Groupe",
                    "Date",
                    "Statut",
                    "Période",
                    "Commentaire",
                ]
            )
            status = {s[0]: s[1] for s in StudentAbsenceTeacherModel.STATUS_CHOICES}
            for a in absences_list:
                row = list(a)
                row[-3] = status[row[-3]]
                writer.writerow(row)
            return response

        if document == "pdf":
            absences_list = absences.values_list(
                "student__last_name",
                "student__first_name",
                "student__classe__year",
                "student__classe__letter",
                "date_absence",
                "status",
                "period__name",
            )

            absences_by_week = [
                {
                    "name": datetime.datetime.strptime(key, "%G-W%V-%u").strftime(
                        "Semaine du %d/%m/%Y"
                    ),
                    "absences": [
                        {
                            "name": cl,
                            "students": [
                                {"name": stud, "status": self._status_by_day(status)}
                                for stud, status in groupby(
                                    sorted(ab, key=lambda a: f"{a[0]}{a[1]}"),
                                    key=lambda a: f"{a[0]} {a[1]}",
                                )
                            ],
                        }
                        for cl, ab in groupby(
                            sorted(value, key=lambda a: f"{a[2]}{a[3]}"),
                            key=lambda a: f"{a[2]}{a[3].upper()}",
                        )  # Group by classe
                    ],
                }
                for key, value in groupby(
                    # Group by week (a[4].isocalendar()[1])
                    absences_list,
                    key=lambda a: f"{a[4].year}-W{a[4].isocalendar()[1]}-1",
                )
            ]
            context = {"weeks": absences_by_week}
            template = get_template("student_absence_teacher/export_pdf.html")
            html_render = template.render(context)

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="export.pdf"'
            HTML(string=html_render).write_pdf(response)
            return response


if "proeco" in settings.INSTALLED_APPS:
    from proeco.views import ExportStudentSelectionAPI

    class ExportStudentAbsenceAPI(ExportStudentSelectionAPI):
        """Export in a file the current list view as a proeco selection."""

        def _get_student_list(self, request, kwargs):
            view_set = StudentAbsenceEducViewSet.as_view({"get": "list"})
            absences = [a["student_id"] for a in view_set(request._request).data["results"]]
            return absences

        def _format_file_name(self, request, **kwargs):
            return "Pref_NOMS_absences.TXT"


class NoJustificationCountAPI(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = [
        "student_absence_teacher.view_justificationmodel",
    ]

    def get(self, request, student=None, format=None):
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)

        core_settings = get_core_settings()
        start = timezone.datetime(
            year=get_scholar_year(),
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        count = StudentAbsenceEducModel.objects.filter(
            justificationmodel__isnull=True,
            student__matricule=student,
            status="A",
            date_absence__gte=start,
        ).count()
        return Response(data={"count": count, "student": int(student)})


class JustificationCountAPI(APIView):
    permission_classes = [IsAuthenticated]
    permission_required = [
        "student_absence_teacher.view_justificationmodel",
    ]

    def get(self, request, student=None, format=None):
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)

        core_settings = get_core_settings()
        start = timezone.datetime(
            year=get_scholar_year(),
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        total_absences_with_just = StudentAbsenceEducModel.objects.filter(
            justificationmodel__isnull=False,
            student__matricule=student,
            status="A",
            date_absence__gte=start,
        )

        justified = (
            total_absences_with_just.filter(justificationmodel__motive__admissible_up_to__gt=0)
            .values(
                "justificationmodel__motive",
                "justificationmodel__motive__short_name",
                "justificationmodel__motive__name",
                "justificationmodel__motive__admissible_up_to",
            )
            .annotate(Count("justificationmodel__motive"))
        )
        unjustified = (
            total_absences_with_just.filter(justificationmodel__motive__admissible_up_to=0)
            .values(
                "justificationmodel__motive",
                "justificationmodel__motive__short_name",
                "justificationmodel__motive__name",
            )
            .annotate(Count("justificationmodel__motive"))
        )

        return Response(
            data={"justified": justified, "unjustified": unjustified, "student": int(student)}
        )


class JustificationFilter(BaseFilters):
    datetime_field = "date_just_start"

    class Meta:
        fields_to_filter = [
            "student__matricule",
            "date_just_start",
            "date_just_end",
            "half_day_start",
            "half_day_end",
            "motive",
        ]
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        model = JustificationModel


class JustificationViewSet(ModelViewSet):
    queryset = JustificationModel.objects.all()
    serializer_class = JustificationSerializer
    permission_classes = [DjangoModelWithAccessPermissions]
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = JustificationFilter
    pagination_class = PageNumberSizePagination
    ordering_fields = [
        "date_just_start",
    ]

    def create(self, request, *args, **kwargs):
        # student_id = request.data.get("student")

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        just = serializer.save()

        if get_settings().sync_with_proeco:
            from libreschoolfdb.writer import set_absence_justification

            teaching_name = StudentModel.objects.get(matricule=just.student.matricule).teaching.name

            server = [
                s["server"] for s in settings.SYNC_FDB_SERVER if s["teaching_name"] == teaching_name
            ]
            if len(server) == 0:
                raise

            set_absence_justification(
                matricule=just.student.matricule,
                just_date_start=just.date_just_start,
                just_date_end=just.date_just_end,
                just_period_start=just.half_day_start,
                just_period_end=just.half_day_end,
                motive=just.motive.short_name,
                comment=just.comment,
                justification="",
                fdb_server=server[0],
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        if get_settings().sync_with_proeco:
            from libreschoolfdb.writer import (
                set_absence_justification,
                change_time_range_absence_justification,
            )

            teaching_name = StudentModel.objects.get(
                matricule=instance.student.matricule
            ).teaching.name

            server = [
                s["server"] for s in settings.SYNC_FDB_SERVER if s["teaching_name"] == teaching_name
            ]
            if len(server) == 0:
                raise

            # Check if dates have changed.
            if (
                serializer.instance.date_just_start != serializer.validated_data["date_just_start"]
                or serializer.instance.date_just_end != serializer.validated_data["date_just_end"]
                or serializer.instance.half_day_start != serializer.validated_data["half_day_start"]
                or serializer.instance.half_day_end != serializer.validated_data["half_day_end"]
            ):
                result = change_time_range_absence_justification(
                    matricule=serializer.validated_data["student"].matricule,
                    old_just_date_start=serializer.instance.date_just_start,
                    old_just_period_start=serializer.instance.half_day_start,
                    old_just_date_end=serializer.instance.date_just_end,
                    old_just_period_end=serializer.instance.half_day_end,
                    just_date_start=serializer.validated_data["date_just_start"],
                    just_period_start=serializer.validated_data["half_day_start"],
                    just_date_end=serializer.validated_data["date_just_end"],
                    just_period_end=serializer.validated_data["half_day_end"],
                    fdb_server=server[0],
                )
                if not result:
                    raise
            else:
                result = set_absence_justification(
                    matricule=serializer.validated_data["student"].matricule,
                    just_date_start=serializer.validated_data["date_just_start"],
                    just_date_end=serializer.validated_data["date_just_end"],
                    just_period_start=serializer.validated_data["half_day_start"],
                    just_period_end=serializer.validated_data["half_day_end"],
                    motive=serializer.validated_data["motive"].short_name,
                    comment=serializer.validated_data["comment"],
                    justification="",
                    fdb_server=server[0],
                )
                if not result[0]:
                    raise

        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # From UpdateMixin class
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if get_settings().sync_with_proeco:
            from libreschoolfdb.writer import remove_absence_justification

            teaching_name = StudentModel.objects.get(
                matricule=instance.student.matricule
            ).teaching.name

            server = [
                s["server"] for s in settings.SYNC_FDB_SERVER if s["teaching_name"] == teaching_name
            ]
            if len(server) == 0:
                raise

            result = remove_absence_justification(
                matricule=instance.student.matricule,
                just_date_start=instance.date_just_start,
                just_date_end=instance.date_just_end,
                just_period_start=instance.half_day_start,
                just_period_end=instance.half_day_end,
                fdb_server=server[0],
            )
            if not result:
                raise

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JustMotiveViewSet(ReadOnlyModelViewSet):
    queryset = JustMotiveModel.objects.all()
    serializer_class = JustMotiveSerializer
    pagination_class = LargePageSizePagination


class MailWarningTemplateAPI(APIView):
    permission_required = [
        "student_absence_teacher.add_justificationmodel",
    ]

    def get(self, request, student_id, date_start, date_end, format=None):
        try:
            student = StudentModel.objects.get(matricule=student_id)
        except ObjectDoesNotExist:
            return Response(None)

        template = MailTemplateModel.objects.get_or_create(name="mail_warning")[0]
        t = Template(template.template)

        c = Context({"student": student, "date_start": date_start, "date_end": date_end})
        return Response(t.render(context=c))


class MailWarningAPI(APIView):
    permission_required = [
        "student_absence_teacher.add_studentabsenceeducmodel",
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
                subject=f"Absence concernant {student.fullname}",
                email_template="student_absence_teacher/email_warning_parents.html",
                context=context,
                reply_to=list(resp_school),
            )

        absences_id = request.data.get("absences")
        for absence in StudentAbsenceEducModel.objects.filter(id__in=absences_id):
            absence.mail_warning = True
            absence.save()

        return Response(status=201)


class WarningPDF(APIView):
    permission_required = [
        "student_absence_teacher.add_studentabsenceeducmodel",
    ]
    renderer_classes = [BinaryFileRenderer]

    def post(self, request, format=None):
        template = get_template("student_absence_teacher/warning_pdf.html")
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


class JustListPDF(LoginRequiredMixin, PermissionRequiredMixin, WeasyTemplateView):
    permission_required = ["student_absence_teacher.view_justificationmodel"]
    template_name = "student_absence_teacher/export_to_just_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = {}
        view_set = StudentAbsenceEducViewSet.as_view({"get": "list"})
        results = view_set(self.request).data["results"]
        matricules = set(map(lambda ab: ab["student"]["matricule"], results))

        group_by_student = [
            [ab for ab in results if ab["student"]["matricule"] == m] for m in matricules
        ]

        classes = set(map(lambda st: st[0]["student"]["classe"]["id"], group_by_student))
        group_by_class = [
            [st for st in group_by_student if st[0]["student"]["classe"]["id"] == c]
            for c in classes
        ]
        group_by_class.sort(
            key=lambda c: (
                c[0][0]["student"]["classe"]["year"],
                c[0][0]["student"]["classe"]["letter"],
            )
        )

        period_dict = {
            p["id"]: p["name"] for p in PeriodEducModel.objects.all().values("id", "name")
        }

        context["absences"] = [
            {
                "className": f"{studentClass[0][0]['student']['classe']['year']}{studentClass[0][0]['student']['classe']['letter'].upper()}",
                "students": sorted(
                    [
                        {
                            "studentName": f"{absences_by_student[0]['student']['last_name']} {absences_by_student[0]['student']['first_name']}",
                            "absences": f"Du {self.get_oldest(absences_by_student, period_dict)} au {self.get_youngest(absences_by_student, period_dict)}",
                        }
                        for absences_by_student in studentClass
                    ],
                    key=lambda st: st["studentName"].upper(),
                ),
            }
            for studentClass in group_by_class
        ]

        return context

    def get_oldest(self, absences, period_dict) -> str:
        oldest = min(absences, key=lambda a: a["date_absence"])
        return f"{oldest['date_absence'][8:10]}/{oldest['date_absence'][5:7]}/{oldest['date_absence'][2:4]} ({period_dict[oldest['period']]})"

    def get_youngest(self, absences, period_dict) -> str:
        youngest = max(absences, key=lambda a: a["date_absence"])
        return f"{youngest['date_absence'][8:10]}/{youngest['date_absence'][5:7]}/{youngest['date_absence'][2:4]} ({period_dict[youngest['period']]})"
