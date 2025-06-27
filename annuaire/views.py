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
import xlsxwriter
from datetime import date, timedelta

from PyPDF2 import PdfWriter
from io import BytesIO

from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q

from rest_framework.views import APIView, Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django_weasyprint import WeasyTemplateView
from unidecode import unidecode

from core.utilities import get_menu, check_student_photo, get_scholar_year
from core.people import People, get_classes
from core.models import (
    StudentModel,
    ClasseModel,
    TeachingModel,
    ResponsibleModel,
    AdditionalStudentInfo,
    CourseModel,
    GivenCourseModel,
)
from core.serializers import (
    StudentSerializer,
    ResponsibleSerializer,
    ClasseSerializer,
    StudentGeneralInfoSerializer,
    StudentContactInfoSerializer,
    StudentMedicalInfoSerializer,
    ResponsibleSensitiveSerializer,
    YearSerializer,
    StudentSensitiveInfoSerializer,
    CourseSerializer,
    GivenCourseSerializer,
)
from core.views import get_app_settings, get_core_settings

from .models import AnnuaireSettingsModel
from .serializers import AnnuaireSettingsSerializer


def get_menu_entry(active_app, request):
    return {
        "app": "annuaire",
        "display": "Annuaire",
        "url": "/annuaire/",
        "active": active_app == "annuaire",
    }


def create_classes_list(request, enseignement="all", check_access=False, annees="", letters=""):
    classes = get_classes([enseignement], check_access, request.user)

    if annees:
        classes = classes.filter(year=annees)

    if letters:
        classes = classes.filter(letter=letters.lower())

    return list(map(lambda c: str(c), classes))


def get_settings():
    return get_app_settings(AnnuaireSettingsModel)


class AnnuaireView(LoginRequiredMixin, TemplateView):
    template_name = "annuaire/annuaire.html"

    def get_context_data(self, **kwargs):
        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context["settings"] = (
            JSONRenderer().render(AnnuaireSettingsSerializer(get_settings()).data).decode()
        )
        context["menu"] = json.dumps(get_menu(self.request, "annuaire"))
        return context


def search_classes(query, teachings, check_access, user):
    if len(query) == 0:
        return []

    if not query[0].isdigit():
        return []

    truncate = True
    classes = get_classes(teaching=teachings, check_access=check_access, user=user)
    classes = classes.filter(year=query[0]).order_by("year", "letter")
    if len(query) > 1:
        classes = classes.filter(letter__icontains=query[1:])

    if truncate:
        classes = classes[:100]

    return ClasseSerializer(classes, many=True, show_teaching=len(teachings) > 1).data


def search_years(query, teachings, check_access, user):
    if len(query) == 0:
        return []

    if not query[0].isdigit():
        return []

    if len(query) > 1:
        if query[1] != "é" or query[1] != "e":
            return []

    years = get_classes(teaching=teachings, check_access=check_access, user=user).distinct(
        "year", "teaching"
    )
    return YearSerializer(
        years.filter(year=query[0]).order_by("year"), many=True, show_teaching=len(teachings) > 1
    ).data


def serialize_people(person):
    if not person:
        return {}
    if type(person) == StudentModel:
        return StudentSerializer(person).data
    elif type(person) == ResponsibleModel:
        return ResponsibleSerializer(person).data


def search_people(
    query,
    people_type,
    teachings,
    check_access,
    user,
    tenure_class_only=True,
    educ_by_years=True,
    active=True,
):
    if len(query) < 1:
        return []

    truncate_limit = 50

    # Check if user can see inactive people. Otherwise revert boolean parameter.
    if active == False:
        annuaire_settings = get_settings()
        if not annuaire_settings.can_see_inactives.all().intersection(user.groups.all()):
            active = True

    people = []
    if people_type == "all":
        classe_years = (
            get_classes(teachings, check_access=True, user=user) if check_access else None
        )

        result = People().get_people_by_name(query, teachings, classes=classe_years, active=active)
        # Check quality.
        if result["student"][1] > result["responsible"][1]:
            people = StudentSerializer(result["student"][0][:truncate_limit], many=True).data
        elif result["responsible"][1] > result["student"][1]:
            people = ResponsibleSerializer(
                result["responsible"][0][:truncate_limit], many=True
            ).data
        else:
            people = (
                StudentSerializer(result["student"][0][: truncate_limit / 2], many=True).data
                + ResponsibleSerializer(
                    result["responsible"][0][: truncate_limit / 2], many=True
                ).data
            )

    if people_type == "student":
        classe_years = (
            get_classes(
                teachings,
                check_access=True,
                user=user,
                tenure_class_only=tenure_class_only,
                educ_by_years=educ_by_years,
            )
            if check_access
            else None
        )
        if query == "everybody":
            students = StudentModel.objects.all()
            if active:
                students = students.filter(inactive_from__isnull=True, classe__isnull=False)
            if classe_years:
                students = students.filter(classe__in=classe_years)
            if teachings and "all" not in teachings:
                if type(teachings[0]) == TeachingModel:
                    students = students.filter(teaching__in=teachings)
                else:
                    students = students.filter(teaching__name__in=teachings)
            truncate_limit = len(students)
        else:
            students = People().get_students_by_name(
                query, teachings, classes=classe_years, active=active
            )[:truncate_limit]

        people = StudentSerializer(students, many=True).data

    if people_type == "responsible":
        people = ResponsibleSerializer(
            People().get_responsibles_by_name(query, teachings, active=active)[:truncate_limit],
            many=True,
        ).data

    if people_type == "teacher":
        people = ResponsibleSerializer(
            People().get_teachers_by_name(query, teachings, active=active)[:truncate_limit],
            many=True,
        ).data

    if people_type == "educator":
        people = ResponsibleSerializer(
            People().get_educators_by_name(query, teachings, active=active)[:truncate_limit],
            many=True,
        ).data

    return people[:truncate_limit]


class SearchPeopleAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        query = request.GET.get("query", "")
        people_type = request.GET.get("people", "all")
        teachings = request.GET.get("teaching", "all")
        check_access = request.GET.get("check_access", False)

        people = search_people(
            query=query,
            people_type=people_type,
            teachings=teachings,
            check_access=check_access,
            user=request.user,
        )
        return Response(people)

    def post(self, request, format=None):
        query = request.data.get("query", "")
        people_type = request.data.get("people", "all")
        teachings = TeachingModel.objects.filter(id__in=request.data.get("teachings", []))
        check_access = request.data.get("check_access", False)
        active = request.data.get("active", True)
        tenure_class_only = request.data.get("tenure_class_only", True)
        educ_by_years = request.data.get("educ_by_years", True)

        people = search_people(
            query=query,
            people_type=people_type,
            teachings=teachings,
            check_access=check_access,
            user=request.user,
            active=active,
            tenure_class_only=tenure_class_only,
            educ_by_years=educ_by_years,
        )
        return Response(people)


class SearchClassesAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        query = request.data.get("query", "")
        teachings = TeachingModel.objects.filter(id__in=request.data.get("teachings", []))
        check_access = request.data.get("check_access", 0) == 1
        years = request.data.get("years", 0) == 1

        classes = search_classes(
            query=query, teachings=teachings, check_access=check_access, user=request.user
        )
        if years:
            classes = (
                search_years(
                    query=query, teachings=teachings, check_access=check_access, user=request.user
                )
                + classes
            )
        return Response(classes)


class SearchClassesOrPeopleAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        query = request.data.get("query", "")
        people_type = request.data.get("people", "student")
        teachings = TeachingModel.objects.filter(id__in=request.data.get("teachings", []))
        check_access = request.data.get("check_access", False)
        active = request.data.get("active", True)

        if len(query) == 0:
            return Response([])

        if query[0].isdigit():
            return Response(
                search_classes(
                    query=query, teachings=teachings, check_access=check_access, user=request.user
                )
            )

        people = search_people(
            query=query,
            people_type=people_type,
            teachings=teachings,
            check_access=check_access,
            user=request.user,
            active=active,
        )
        return Response(people)


class StudentClasseAPI(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self, request, format=None):
        classe_id = request.GET.get("classe", None)
        gender = request.GET.get("gender", None)
        print(gender)
        if not classe_id or not classe_id.isdigit:
            return Response([])

        students = StudentModel.objects.filter(classe__id=classe_id).order_by(
            "last_name", "first_name"
        )
        if gender:
            students = students.filter(additionalstudentinfo__gender=gender)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)


class StudentGivenCourseAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, given_course_id, format=None):
        try:
            given_course = GivenCourseModel.objects.get(id=given_course_id)
            students = StudentModel.objects.filter(
                courses=given_course, classe__isnull=False
            ).order_by("last_name", "first_name")
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response([])


class CourseToClassesAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, given_course_id, format=None):
        try:
            course = GivenCourseModel.objects.get(id=given_course_id)
            classes = course.studentmodel_set.distinct("classe").values_list(
                "classe__year", "classe__letter"
            )
            return Response(
                [f"{classe_year}{classe_letter}" for (classe_year, classe_letter) in classes]
            )
        except ObjectDoesNotExist:
            return Response([])


class AnnuaireSettingsViewSet(ModelViewSet):
    queryset = AnnuaireSettingsModel.objects.all()
    serializer_class = AnnuaireSettingsSerializer
    permission_classes = (IsAdminUser,)


class StudentInfoViewSet(ReadOnlyModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        kwargs["no_course"] = False
        return serializer_class(*args, **kwargs)


class ResponsibleInfoViewSet(ReadOnlyModelViewSet):
    queryset = ResponsibleModel.objects.all()
    serializer_class = ResponsibleSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "matricule"


class ResponsibleSensitiveViewSet(ReadOnlyModelViewSet):
    queryset = ResponsibleModel.objects.all()
    serializer_class = ResponsibleSensitiveSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "matricule"

    def get_queryset(self):
        allowed_groups = get_settings().can_see_responsibles_sensitive.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return ResponsibleModel.objects.none()

        return super().get_queryset()


class StudentGeneralInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentGeneralInfoSerializer
    permission_classes = (IsAuthenticated,)


class StudentSensitiveInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentSensitiveInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allowed_groups = get_settings().can_see_student_sensitive.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return AdditionalStudentInfo.objects.none()

        return super().get_queryset()


class StudentContactInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentContactInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allowed_groups = get_settings().can_see_student_contact.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return AdditionalStudentInfo.objects.none()

        return super().get_queryset()


class StudentMedicalInfoViewSet(ReadOnlyModelViewSet):
    queryset = AdditionalStudentInfo.objects.all()
    serializer_class = StudentMedicalInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        allowed_groups = get_settings().can_see_student_medical.all()
        if not self.request.user.groups.intersection(allowed_groups).exists():
            return AdditionalStudentInfo.objects.none()

        return super().get_queryset()


class ClasseListExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        classe_id = self.request.GET.get("classe_id")
        course_id = self.request.GET.get("course_id")
        list_type = self.request.GET.get("list_type", "login")

        if classe_id:
            try:
                classe = ClasseModel.objects.get(id=classe_id)
            except ObjectDoesNotExist:
                # Class not found
                return render(request, "dossier_eleve/no_student.html")

            students = StudentModel.objects.filter(classe=classe).order_by(
                "last_name", "first_name"
            )
            file_name = "classes_%s_%s%s.xlsx" % (classe.teaching.name, classe.year, classe.letter)
        elif course_id:
            given_course = GivenCourseModel.objects.get(id=course_id)
            students = StudentModel.objects.filter(courses=given_course)
            file_name = f"cours_{given_course.course.short_name.replace(' ', '-')}.xlsx"

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 6, 30)

        headers = ["Nom", "Prénom", "Classe"]
        if list_type == "login":
            headers += ["Nom d'utilisateur", "Mot de passe"]
        elif list_type == "info":
            headers += ["Genre", "Orientation", "Langue 1"]

        row_number = 0
        worksheet.write_row(0, 0, headers)
        row_number += 1
        for s in students:
            row = [s.last_name, s.first_name, s.classe.compact_str]
            if not s.additionalstudentinfo:
                worksheet.write(row_number, 0, row)
            else:
                if list_type == "login":
                    row += [
                        s.additionalstudentinfo.username,
                        s.additionalstudentinfo.password,
                    ]
                elif list_type == "info":
                    row += [
                        s.additionalstudentinfo.gender,
                        s.additionalstudentinfo.orientation,
                    ]

                worksheet.write_row(row_number, 0, row)
            row_number += 1
        workbook.close()

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'filename; filename="' + file_name + '"'
        response.write(output.getvalue())
        return response


class ClasseListPDF(WeasyTemplateView, LoginRequiredMixin):
    template_name = "annuaire/classe_list_pdf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        classe_id = kwargs["classe_id"]
        try:
            classe = ClasseModel.objects.get(id=classe_id)
            context["classe"] = classe
        except ObjectDoesNotExist:
            # Class not found
            context["classe"] = None
            return context

        context["students"] = StudentModel.objects.filter(classe=classe).order_by(
            "last_name", "first_name"
        )
        context["students_numb"] = len(context["students"])
        context["tenures"] = ResponsibleModel.objects.filter(tenure=classe)

        return context


class ClassePhotosView(LoginRequiredMixin, WeasyTemplateView):
    template_name = "annuaire/classe_photos.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        classe_id = self.request.GET.get("classe_id")
        course_id = self.request.GET.get("course_id")

        if classe_id:
            try:
                classe = ClasseModel.objects.get(id=classe_id)
                students = StudentModel.objects.filter(classe=classe)
                title = classe.compact_str
                tenures = ResponsibleModel.objects.filter(tenure=classe)

                context["tenures"] = tenures
            except ObjectDoesNotExist:
                return context
        elif course_id:
            try:
                given_course = GivenCourseModel.objects.get(id=course_id)
                students = StudentModel.objects.filter(courses=given_course)
                title = f"{given_course.course.long_name} ({given_course.classes})"
            except ObjectDoesNotExist:
                return context
        else:
            return context

        students = sorted(students, key=lambda s: unidecode(s.last_name.lower()))
        rows = []
        student_by_row = 6
        row = []
        for i, student in enumerate(students):
            check_student_photo(student)
            if i % student_by_row == 0:
                row = []
            row.append(student)
            if i % student_by_row == student_by_row - 1 or len(students) == i + 1:
                rows.append(row)

        context["title"] = title
        context["list"] = rows
        context["students_numb"] = len(students)

        return context


class SummaryPDF(WeasyTemplateView, PermissionRequiredMixin):
    template_name = "annuaire/summary.html"

    def get_permission_required():
        permission_required = []

        if "dossier_eleve" in settings.INSTALLED_APPS:
            permission_required.append("dossier_eleve.view_caseleve")

        if "lateness" in settings.INSTALLED_APPS:
            permission_required.append("lateness.view_latenessmodel")

        if "student_absence_teacher" in settings.INSTALLED_APPS:
            permission_required += [
                "student_absence_teacher.view_studentabsenceteachermodel",
                "student_absence_teacher.view_studentabsenceeducmodel",
                "student_absence_teacher.view_justificationmodel",
            ]

    def get(self, request, *args, **kwargs):
        annuaire_settings = get_settings()
        if (
            not annuaire_settings.can_see_summary.all()
            .intersection(request.user.groups.all())
            .exists()
        ):
            return HttpResponse("Pas d'accès autorisé")

        if kwargs["category"] == "student":
            return self.render_to_response(self.get_student_context(**kwargs))

        elif kwargs["category"] == "class":
            classModel = ClasseModel.objects.get(id=kwargs["id"])
            students = People().get_students_by_classe(classModel)
            if not students:
                return render(request, "dossier_eleve/no_student.html")

            merger = PdfWriter()
            for s in students:
                kwargs["id"] = s.matricule
                student_context = self.get_student_context(**kwargs)
                if not student_context:
                    continue
                student_response = self.render_to_response(student_context)
                pdf = BytesIO(student_response.rendered_content)
                if not pdf:
                    continue

                merger.append(pdf)

            output_stream = BytesIO()
            merger.write(output_stream)
            merger.close()
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                'filename; filename="' + classModel.compact_str + '.pdf"'
            )
            response.write(output_stream.getvalue())
            return response

    def get_student_context(self, **kwargs) -> dict:
        context = {}

        date_from = date(
            int(kwargs["date_from"][:4]),
            int(kwargs["date_from"][5:7]),
            int(kwargs["date_from"][8:]),
        )
        date_to = date(
            int(kwargs["date_to"][:4]), int(kwargs["date_to"][5:7]), int(kwargs["date_to"][8:])
        )

        context["date_from"] = date_from
        context["date_to"] = date_to

        core_settings = get_core_settings()
        scholar_year_start = timezone.datetime(
            year=get_scholar_year(),
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        scholar_year_end = scholar_year_start + timezone.timedelta(days=350)

        try:
            student = StudentModel.objects.get(matricule=kwargs["id"])
            context["student"] = student
        except ObjectDoesNotExist:
            return {}

        if "dossier_eleve" in settings.INSTALLED_APPS:
            from dossier_eleve.views import StatisticAPI
            from dossier_eleve.models import CasEleve

            context["dossier_eleve"] = {
                "statistics": StatisticAPI().gen_stats(
                    self.request.user, student, only_sanctions=True, only_asked_sanctions=True
                ),
                "last_entries": CasEleve.objects.filter(
                    student=student,
                    date_sanction__gte=date_from,
                    date_sanction__lte=date_to,
                    sanction_decision__isnull=False,
                    sanction_decision__can_ask=True,
                ).order_by("date_sanction"),
            }

        if "lateness" in settings.INSTALLED_APPS:
            from lateness.models import LatenessModel

            context["lateness"] = {
                "scholar_year": {
                    "justified": LatenessModel.objects.filter(
                        student=student,
                        justified=True,
                        datetime_creation__gte=scholar_year_start,
                        datetime_creation__lte=scholar_year_end,
                    ).count(),
                    "unjustified": LatenessModel.objects.filter(
                        student=student,
                        justified=False,
                        datetime_creation__gte=scholar_year_start,
                        datetime_creation__lte=scholar_year_end,
                    ).count(),
                },
                "last_entries": LatenessModel.objects.filter(
                    student=student,
                    datetime_creation__gte=date_from,
                    datetime_creation__lte=date_to,
                ).order_by("datetime_creation"),
            }

        if "student_absence_teacher" in settings.INSTALLED_APPS:
            from student_absence_teacher.views import JustificationCountAPI
            from student_absence_teacher.models import (
                JustificationModel,
                StudentAbsenceTeacherModel,
            )

            context["student_absence_teacher"] = {
                "absences": JustificationCountAPI.as_view()(
                    request=self.request, student=student.matricule
                ).data,
                "last_just": JustificationModel.objects.filter(
                    student=student, date_just_start__gte=date_from, date_just_end__lte=date_to
                ),
                "exclusions": StudentAbsenceTeacherModel.objects.filter(
                    student=student,
                    date_absence__gte=scholar_year_start,
                    date_absence__lte=scholar_year_end,
                    status=StudentAbsenceTeacherModel.EXCLUDED,
                ).count(),
                "last_exclusions": StudentAbsenceTeacherModel.objects.filter(
                    student=student,
                    date_absence__gte=date_from,
                    date_absence__lte=date_to,
                    status=StudentAbsenceTeacherModel.EXCLUDED,
                ),
            }
        return context

class YellowpageAPI(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, phonenum, format=None):
        students = StudentModel.objects.filter(
            Q(additionalstudentinfo__resp_mobile__iexact=phonenum)| 
            Q(additionalstudentinfo__resp_phone__iexact=phonenum)|
            Q(additionalstudentinfo__father_mobile__iexact=phonenum)|
            Q(additionalstudentinfo__father_phone__iexact=phonenum)|
            Q(additionalstudentinfo__mother_mobile__iexact=phonenum)|
            Q(additionalstudentinfo__mother_phone__iexact=phonenum)|
            Q(additionalstudentinfo__student_mobile__iexact=phonenum)
            )
        serializer = StudentSerializer(students,many=True)
        #serializer = StudentContactInfoSerializer(students, many=True)
        return Response(serializer.data)

class EmailSearcherAPI(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, email, format=None):
        students = StudentModel.objects.filter(
            Q(additionalstudentinfo__resp_email__iexact=email)| 
            Q(additionalstudentinfo__mother_email__iexact=email)|
            Q(additionalstudentinfo__father_email__iexact=email)|
            Q(additionalstudentinfo__student_email__iexact=email)
            )
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data)

class CourseAPI(APIView):
    def get(self,request,keyword,format=None):
        course = CourseModel.objects.filter(
            Q(long_name__icontains=keyword)|
            Q(short_name__icontains=keyword)
            )
        serializer = CourseSerializer(course,many=True)
        return Response(serializer.data)

class GivenCourseAPI(APIView):
    def get(self,request,course_id,format=None):
        given_course = GivenCourseModel.objects.filter(course = course_id)
        serializer = GivenCourseSerializer(given_course, many=True)
        return Response(serializer.data)