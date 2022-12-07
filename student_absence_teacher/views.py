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

from django.template.loader import get_template
from django.db.models import Count, ObjectDoesNotExist
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse

from django_filters import rest_framework as filters

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter

from core.models import ClasseModel, StudentModel, ResponsibleModel
from core.utilities import get_menu, get_scholar_year
from core.people import get_classes
from core.views import BaseFilters, PageNumberSizePagination

from .models import StudentAbsenceTeacherSettingsModel, StudentAbsenceTeacherModel, PeriodModel, LessonModel
from .serializers import StudentAbsenceTeacherSettingsSerializer, PeriodSerializer, StudentAbsenceTeacherSerializer


def get_menu_entry(active_app: str, request) -> dict:
    if not request.user.has_perm('student_absence_teacher.view_studentabsenceteachermodel'):
        return {}
    return {
            "app": "student_absence_teacher",
            "display": "Abs. Élèves (prof)",
            "url": "/student_absence_teacher",
            "active": active_app == "student_absence_teacher"
    }


def get_settings():
    settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.first()
    if not settings_student_absence:
        # Create default settings.
        settings_student_absence = StudentAbsenceTeacherSettingsModel.objects.create().save()

    return settings_student_absence


class StudentAbsenceTeacherView(LoginRequiredMixin,
                                PermissionRequiredMixin,
                                TemplateView):
    template_name = "student_absence_teacher/student_absence_teacher.html"
    permission_required = ('student_absence_teacher.view_studentabsenceteachermodel')
    filters = [
        {'value': 'student__display', 'text': 'Nom'},
        {'value': 'student__matricule', 'text': 'Matricule'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'period__name', 'text': 'Période'},
        {'value': 'activate_absent', 'text': 'Absents'},
        {'value': 'date_absence', 'text': 'Date'},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['menu'] = json.dumps(get_menu(self.request, "student_absence_absence"))
        context['filters'] = json.dumps(self.filters)
        context['settings'] = json.dumps((StudentAbsenceTeacherSettingsSerializer(get_settings()).data))
        context["proeco"] = json.dumps("proeco" in settings.INSTALLED_APPS)

        return context


class StudentAbsenceTeacherFilter(BaseFilters):
    student__display = filters.CharFilter(method='people_name_by')
    classe = filters.CharFilter(method='classe_by')
    activate_absent = filters.BooleanFilter(method="activate_absent_by")

    class Meta:
        fields_to_filter = [
            'student', 'date_absence', 'student__matricule', 'student__classe', "period", "period__name",
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
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = StudentAbsenceTeacherFilter
    ordering_fields = ['date_absence', 'datetime_update', 'datetime_creation', 'period']
    pagination_class = PageNumberSizePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PeriodViewSet(ReadOnlyModelViewSet):
    queryset = PeriodModel.objects.all().order_by("start")
    serializer_class = PeriodSerializer


class OverviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def _extract_count_from_educator(self, classe, absences, periods, date):
        counts = {
            "classe": classe.compact_str,
            "classe__id": classe.id
        }

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
                teacher_count = teacher_abs_period.filter(
                    status=StudentAbsenceTeacherModel.ABSENCE
                ).distinct("student").count()
            else:
                teacher_count = -1
            counts[f"period-{period.id}"] = {"teacher_count": teacher_count}
            # Hu?
            counts[f"period-{period.id}"]["not_teacher_count"] = next(
                (x["id__count"] for x in absences \
                    if x["period"] == period.id and x["is_absent"]),
                next((0 for y in absences if y["period"] == period.id), -1)
            )
        return counts

    def _extract_count_from_teacher(self, classe, absences, periods, date):
        counts = {
            "classe": classe.compact_str,
            "classe__id": classe.id
        }

        use_student_absence = "student_absence" in settings.INSTALLED_APPS
        if use_student_absence:
            from student_absence.models import StudentAbsenceModel
        not_teacher_abs = StudentAbsenceModel.objects.filter(student__classe=classe, date_absence=date)

        for period in periods:
            if use_student_absence:
                not_teacher_period = not_teacher_abs.filter(
                    period__start__lt=period.end, period__end__gt=period.start
                )
                if not_teacher_period.count() > 0:
                    not_teacher_count = not_teacher_period.filter(is_absent=True).count()
                else:
                    not_teacher_count = -1
                counts[f"period-{period.id}"] = {"not_teacher_count": not_teacher_count}
            counts[f"period-{period.id}"]["teacher_count"] = next(
                (x["id__count"] for x in absences \
                    if x["period"] == period.id and x["status"] == StudentAbsenceTeacherModel.ABSENCE),
                next((0 for y in absences if y["period"] == period.id), -1)
            )

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
                educ_by_years="both"
            ).order_by("year", "letter")

        if point_of_view == "teacher":
            periods = PeriodModel.objects.order_by("start")
            count_by_classe_by_period = [
                self._extract_count_from_teacher(
                    c,
                    StudentAbsenceTeacherModel.objects \
                        ## Exclude only LATENESS ????
                        .exclude(status=StudentAbsenceTeacherModel.LATENESS) \
                        .filter(date_absence=date, student__classe=c) \
                        .values("period", "status").annotate(Count("id")),
                    periods,
                    date
                )
                for c in classes
            ]

            return Response(json.dumps(count_by_classe_by_period))
        elif point_of_view == "educator":
            if "student_absence" not in settings.INSTALLED_APPS:
                return Response(json.dumps({}))

            from student_absence.models import StudentAbsenceModel, PeriodModel as PeriodModelEducator

            periods = PeriodModelEducator.objects.order_by("start")
            count_by_classe_by_period = [
                self._extract_count_from_educator(
                    c,
                    StudentAbsenceModel.objects
                    .filter(date_absence=date, student__classe=c)
                    .values("period", "is_absent").annotate(Count("id")),
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
        ).exclude(
            status=StudentAbsenceTeacherModel.PRESENCE
        )

        # If user cannot see list (overview), only show own absences.
        if not get_settings().can_see_list.filter(id__in=[g.id for g in request.user.groups.all()]).exists():
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
            writer.writerow([
                "Matricule unique",
                "Nom",
                "Prénom",
                "Année",
                "Classe",
                "Groupe",
                "Date",
                "Statut",
                "Période"
                "Commentaire"
            ])
            status = {s[0]: s[1] for s in StudentAbsenceTeacherModel.STATUS_CHOICES}
            for a in absences_list:
                row = list(a)
                row[-2] = status[row[-2]]
                writer.writerow(
                    row
                )
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
                    "name": datetime.datetime.strptime(key, '%G-W%V-%u').strftime("Semaine du %d/%m/%Y"),
                    "absences": [
                        {
                            "name": cl,
                            "students": [
                                {
                                    "name": stud,
                                    "status": self._status_by_day(status)
                                }
                                for stud, status in groupby(
                                    sorted(ab, key=lambda a: f"{a[0]}{a[1]}"),
                                    key=lambda a: f"{a[0]} {a[1]}"
                                )
                            ]
                        }
                        for cl, ab in groupby(
                            sorted(value, key=lambda a: f"{a[2]}{a[3]}"),
                            key=lambda a: f"{a[2]}{a[3].upper()}"
                        )  # Group by classe
                    ]

                }
                for key, value in groupby(
                    # Group by week (a[4].isocalendar()[1])
                    absences_list, key=lambda a: f"{a[4].year}-W{a[4].isocalendar()[1]}-1"
                )
            ]
            context = {"weeks": absences_by_week}
            template = get_template("student_absence_teacher/export_pdf.html")
            html_render = template.render(context)

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="export.pdf"'
            HTML(string=html_render).write_pdf(response)
            return response
