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

from io import BytesIO

from django.conf import settings
from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView, Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django_weasyprint import WeasyTemplateView
from z3c.rml import rml2pdf
from unidecode import unidecode

from core.utilities import get_menu, check_student_photo
from core.people import People, get_classes
from core.models import (
    StudentModel,
    ClasseModel,
    TeachingModel,
    ResponsibleModel,
    AdditionalStudentInfo,
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
    GivenCourseModel,
)
from core.views import get_app_settings

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
        check_access = request.GET.get("check_access", "0") == 1

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
        check_access = request.data.get("check_access", 0) == 1
        active = request.data.get("active", 1) == 1
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
        check_access = request.data.get("check_access", 0) == 1
        active = request.data.get("active", 1) == 1

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
        classe_id = kwargs["classe_id"]
        try:
            classe = ClasseModel.objects.get(id=classe_id)
        except ObjectDoesNotExist:
            # Class not found
            return render(request, "dossier_eleve/no_student.html")

        students = StudentModel.objects.filter(classe=classe).order_by("last_name", "first_name")
        file_name = "classes_%s_%s%s.xlsx" % (classe.teaching.name, classe.year, classe.letter)
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 2, 30)

        row = 0
        worksheet.write_row(0, 0, ["Nom et prénom", "Nom d'utilisateur", "Mot de passe"])
        row += 1
        for s in students:
            if not s.additionalstudentinfo:
                worksheet.write(row, 0, s.fullname)
            else:
                worksheet.write_row(
                    row,
                    0,
                    [
                        s.fullname,
                        s.additionalstudentinfo.username,
                        s.additionalstudentinfo.password,
                    ],
                )
            row += 1
        workbook.close()

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'filename; filename="' + file_name + '"'
        response.write(output.getvalue())
        return response


class ClasseListPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        classe_id = kwargs["classe_id"]
        try:
            classe = ClasseModel.objects.get(id=classe_id)
        except ObjectDoesNotExist:
            # Class not found
            return render(request, "dossier_eleve/no_student.html")

        students = StudentModel.objects.filter(classe=classe).order_by("last_name", "first_name")
        tenures = ResponsibleModel.objects.filter(tenure=classe)
        t = get_template("annuaire/classe_list.rml")
        rml_str = t.render(
            {
                "students": students,
                "students_numb": len(students),
                "classe": classe,
                "tenures": tenures,
            }
        )

        pdf = rml2pdf.parseString(rml_str)
        if not pdf:
            return render(request, "dossier_eleve/no_student.html")
        pdf_name = "classes_%s_%s%s.pdf" % (classe.teaching.name, classe.year, classe.letter)

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'filename; filename="' + pdf_name + '"'
        response.write(pdf.read())
        return response


class ClassePhotosView(LoginRequiredMixin, WeasyTemplateView):
    template_name = "annuaire/classe_photos.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        classe_id = kwargs["classe_id"]
        try:
            classe = ClasseModel.objects.get(id=classe_id)
        except ObjectDoesNotExist:
            return context
        students = StudentModel.objects.filter(classe=classe)

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

        context = {"classe": classe.compact_str, "list": rows, "students_numb": len(students)}

        tenures = ResponsibleModel.objects.filter(tenure=classe)

        context["tenures"] = tenures
        return context
