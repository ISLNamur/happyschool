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
import warnings
import requests
import os
import calendar
import itertools
import copy

from datetime import date, timedelta

from icalendar import Calendar

from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django_filters import rest_framework as filters

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import CharField, Q
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.views.generic import TemplateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.middleware.csrf import get_token
from django.conf import settings

from core.models import (
    ResponsibleModel,
    TeachingModel,
    EmailModel,
    CoreSettingsModel,
    StudentModel,
    ImportCalendarModel,
    ClasseModel,
    CourseModel,
    GivenCourseModel,
)
from core.people import get_classes
from core.permissions import IsSecretaryPermission
from core.serializers import (
    ResponsibleSensitiveSerializer,
    TeachingSerializer,
    EmailSerializer,
    ClasseSerializer,
    ResponsibleRemoteSerializer,
    StudentWriteSerializer,
    UserSerializer,
    GroupSerializer,
    CourseSerializer,
    GivenCourseFlatSerializer,
    CourseScheduleModel,
    PeriodCoreModel,
    PeriodCoreSerializer,
    CourseScheduleSerializer,
    GivenCourseSerializer,
)
from core.utilities import get_scholar_year, get_menu


def get_app_settings(SettingsModel):
    settings_model = SettingsModel.objects.first()
    if not settings_model:
        # Create default settings.
        settings_model = SettingsModel()
        settings_model.save()
    return settings_model


def get_core_settings():
    return get_app_settings(CoreSettingsModel)


class BaseFilters(filters.FilterSet):
    datetime_field = "datetime_encodage"
    student_field = "student"

    unique = filters.CharFilter("unique_by", method="unique_by")
    scholar_year = filters.CharFilter(method="scholar_year_by")
    activate_own_classes = filters.BooleanFilter(method="activate_own_classes_by")

    class Meta:
        fields_to_filter = set()

        def generate_filters(fields) -> dict:
            filters = {}
            for f in fields:
                is_date_or_time = f.startswith("date") or f.startswith("time")
                filters[f] = (
                    ["exact"] if not is_date_or_time else ["lt", "gt", "lte", "gte", "exact"]
                )
            return filters

        fields = generate_filters(fields_to_filter)
        filter_overrides = {
            CharField: {
                "filter_class": filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "unaccent__icontains",
                },
            },
        }

    def unique_by(self, queryset, field_name, value):
        if value:
            # Distinct query in postgrsql asks to order_by the same column.
            return queryset.order_by(value).distinct(value)
        else:
            return queryset

    def scholar_year_by(self, queryset, field_name, value):
        start_year = int(value[:4])
        core_settings = get_core_settings()
        start = timezone.datetime(
            year=start_year,
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        end = start + timezone.timedelta(days=355)
        return queryset.filter(
            **{self.datetime_field + "__gte": start, self.datetime_field + "__lte": end}
        )

    def classe_by(self, queryset, field_name, value):
        if not value:
            return queryset
        if not value[0].isdigit():
            return queryset

        classe = value.split(",") if "," in value else [value]
        query_filter = Q()
        for c in classe:
            current_filter = Q(**{self.student_field + "__classe__year": c[0]})
            if len(c) > 1:
                current_filter = current_filter & Q(
                    **{self.student_field + "__classe__letter__istartswith": c[1:]}
                )
            query_filter = query_filter | current_filter
        return queryset.filter(query_filter)

    def people_name_by(self, queryset, name, value):
        tokens = value.split(" ")
        people = queryset.none()

        if len(tokens) > 1:
            # First check compound last name.
            people = queryset.filter(
                Q(
                    **{
                        f"{self.student_field}__last_name__unaccent__istartswith": " ".join(
                            tokens[:2]
                        )
                    }
                )
                | Q(
                    **{
                        f"{self.student_field}__last_name__unaccent__istartswith": " ".join(
                            tokens[-2:]
                        )
                    }
                )
            )
            if len(people) == 0:
                people = queryset.filter(
                    Q(
                        **{
                            f"{self.student_field}__first_name__unaccent__iexact": tokens[0],
                            f"{self.student_field}__last_name__unaccent__istartswith": tokens[1],
                        }
                    )
                    | Q(
                        **{
                            f"{self.student_field}__first_name__unaccent__istartswith": tokens[1],
                            f"{self.student_field}__last_name__unaccent__iexact": tokens[0],
                        }
                    )
                )

        if len(people) == 0:
            for name_part in tokens:
                people |= queryset.filter(
                    Q(**{f"{self.student_field}__first_name__unaccent__istartswith": name_part})
                    | Q(**{f"{self.student_field}__last_name__unaccent__istartswith": name_part})
                )
        return people

    def activate_own_classes_by(self, queryset, name, value):
        if not value:
            return queryset

        resp = ResponsibleModel.objects.get(user=self.request.user)
        classes = get_classes(
            teaching=resp.teaching.all(),
            check_access=True,
            user=self.request.user,
            tenure_class_only=False,
            educ_by_years="both",
        ).order_by("year", "letter")

        return queryset.filter(**{f"{self.student_field}__classe__id__in": [c.id for c in classes]})


class PageNumberSizePagination(PageNumberPagination):
    """
    Offer a query parameter (page_size) to fix page size for pagination.
    Default is still 20 items.
    """

    page_size_query_param = "page_size"
    max_page_size = 5000


class LargePageSizePagination(PageNumberPagination):
    """
    Pagination with a default page size of 500 items and a query parameter (page_size).
    """

    page_size = 500


class DjangoModelWithAccessPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]


class LoginView(DjangoLoginView):
    template_name = "core/auth.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["csrf_token"] = get_token(self.request)
        context["google"] = (
            "social_core.backends.google.GoogleOAuth2" in settings.AUTHENTICATION_BACKENDS
        )
        context["microsoft"] = (
            "social_core.backends.microsoft.MicrosoftOAuth2" in settings.AUTHENTICATION_BACKENDS
        )
        context["model"] = (
            "django.contrib.auth.backends.ModelBackend" in settings.AUTHENTICATION_BACKENDS
        )

        return context


class BaseModelViewSet(ModelViewSet):
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    permission_classes = (DjangoModelWithAccessPermissions,)
    pagination_class = PageNumberSizePagination
    user_field = None
    username_field = "user"

    def get_queryset(self):
        if self.request.user.groups.intersection(self.get_group_all_access()).exists():
            return self.queryset
        else:
            stud_teach_rel = get_core_settings().student_teacher_relationship
            try:
                responsible = ResponsibleModel.objects.get(user=self.request.user)

                if stud_teach_rel == CoreSettingsModel.BY_CLASSES or self.is_only_tenure():
                    teachings = responsible.teaching.all()
                    classes = get_classes(
                        list(map(lambda t: t.name, teachings)),
                        True,
                        self.request.user,
                        tenure_class_only=self.is_only_tenure(),
                    ).values_list("id")
                    try:
                        queryset = self.queryset.filter(student__classe__id__in=classes)
                    except FieldError:
                        queryset = self.queryset.filter(matricule__classe__id__in=classes)
                        warnings.warn(
                            "Use *student* as field name instead of matricule", DeprecationWarning
                        )
                elif stud_teach_rel == CoreSettingsModel.BY_COURSES:
                    try:
                        queryset = self.queryset.filter(
                            student__courses__in=responsible.courses.all()
                        )
                    except FieldError:
                        queryset = self.queryset.filter(
                            matricule__courses__in=responsible.courses.all()
                        )
                        warnings.warn(
                            "Use *student* as field name instead of matricule", DeprecationWarning
                        )
                elif stud_teach_rel == CoreSettingsModel.BY_CLASSES_COURSES:
                    teachings = responsible.teaching.all()
                    classes = get_classes(
                        list(map(lambda t: t.name, teachings)),
                        True,
                        self.request.user,
                        tenure_class_only=self.is_only_tenure(),
                    ).values_list("id")
                    queryset = self.queryset.filter(
                        Q(matricule__classe__id__in=classes)
                        | Q(matricule__courses__in=responsible.courses.all())
                    )
            except ObjectDoesNotExist:
                return self.queryset.none()
            return queryset

    def perform_create(self, serializer):
        serializer.save()
        if self.username_field:
            serializer.save(
                **{
                    self.username_field: self.request.user.username,
                }
            )
        if self.user_field:
            serializer.save(
                **{
                    self.user_field: self.request.user,
                }
            )

    def get_group_all_access(self):
        return Group.objects.none()

    def is_only_tenure(self):
        return True


class MembersView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "core/members.html"
    permission_required = "core.add_responsiblemodel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = json.dumps(get_menu(self.request))
        return context


class BaseUploadFileView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)
    file_model = None
    file_serializer = None

    def get(self, request, pk, format=None):
        try:
            attachment = self.file_model.objects.get(pk=pk)
            serializer = self.file_serializer(attachment)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        file_obj = request.FILES["file"]
        attachment = self.file_model(attachment=file_obj)
        attachment.save()
        serializer = self.file_serializer(attachment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            attachment = self.file_model.objects.get(pk=pk)
            attachment.delete()
            if os.path.isfile(attachment.attachment.path):
                os.remove(attachment.attachment.path)
        except ObjectDoesNotExist:
            pass

        # As we want the object to be removed, if it's not found, it's ok!
        return Response(status=status.HTTP_200_OK)


class ProfilView(LoginRequiredMixin, TemplateView):
    template_name = "core/profil.html"


class MembersAPI(ModelViewSet):
    queryset = ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)
    serializer_class = ResponsibleSensitiveSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )

    def get_queryset(self):
        person_type = self.request.GET.get("person_type", None)
        if person_type == "secretary":
            return ResponsibleModel.objects.filter(is_secretary=True)
        elif person_type == "others":
            return ResponsibleModel.objects.filter(
                is_teacher=False, is_educator=False, is_secretary=False
            )
        else:
            return ResponsibleModel.objects.filter(is_teacher=False, is_educator=False)


class ScholarYearAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        current_year = get_scholar_year()
        options = []
        for y in reversed(range(current_year - 10, current_year + 1)):
            options.append("%i-%i" % (y, y + 1))
        return Response(options)


class TeachingViewSet(ModelViewSet):
    queryset = TeachingModel.objects.all()
    serializer_class = TeachingSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated, DjangoModelPermissions]
        return [permission() for permission in permission_classes]


class ClasseViewSet(ModelViewSet):
    queryset = ClasseModel.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class CourseViewSet(ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class GivenCourseViewSet(ModelViewSet):
    queryset = GivenCourseModel.objects.all()
    serializer_class = GivenCourseFlatSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class GivenCourseInfoViewSet(ReadOnlyModelViewSet):
    queryset = GivenCourseModel.objects.all()
    serializer_class = GivenCourseSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course"]


class ResponsibleViewSet(ModelViewSet):
    queryset = ResponsibleModel.objects.all()
    serializer_class = ResponsibleRemoteSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class StudentViewSet(ModelViewSet):
    queryset = StudentModel.objects.all()
    serializer_class = StudentWriteSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class EmailViewSet(ReadOnlyModelViewSet):
    queryset = EmailModel.objects.all().order_by("display")
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargePageSizePagination


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthenticated,
        DjangoModelPermissions,
    )
    pagination_class = LargePageSizePagination


class CourseScheduleFilter(filters.FilterSet):
    student = filters.NumberFilter(method="student_by")
    responsible = filters.NumberFilter(method="responsible_by")
    classe = filters.NumberFilter(method="classe_by")

    class Meta:
        fields = ["given_course", "place"]

    def student_by(self, queryset, field_name, value):
        try:
            student = StudentModel.objects.get(matricule=value)
            given_courses = [gc.id for gc in student.courses.all()]
            return queryset.filter(given_course__id__in=given_courses)
        except ObjectDoesNotExist:
            return queryset.none()

    def responsible_by(self, queryset, field_name, value):
        try:
            resp = ResponsibleModel.objects.get(matricule=value)
            given_courses = [gc.id for gc in resp.courses.all()]
            return queryset.filter(given_course__id__in=given_courses).distinct()
        except ObjectDoesNotExist:
            return queryset.none()

    def classe_by(self, queryset, field_name, value):
        try:
            classe = ClasseModel.objects.get(id=value)
            related_students = StudentModel.objects.filter(classe=classe)
            given_courses = [gc.id for student in related_students for gc in student.courses.all()]
            return queryset.filter(given_course__id__in=given_courses)
        except ObjectDoesNotExist:
            return queryset.none()


class CourseScheduleViewSet(ModelViewSet):
    queryset = CourseScheduleModel.objects.all()
    serializer_class = CourseScheduleSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargePageSizePagination
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = CourseScheduleFilter
    ordering_fields = ["day_of_week", "period__start", "period__end"]
    ordering = ["day_of_week", "period__start", "period__end"]


class PeriodCoreViewSet(ModelViewSet):
    queryset = PeriodCoreModel.objects.all()
    serializer_class = PeriodCoreSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LargePageSizePagination


class BirthdayAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        people = self.request.GET.get("people", "student")

        birthday = []
        today = timezone.now()
        if people == "student":
            students = StudentModel.objects.filter(
                additionalstudentinfo__birth_date__month=today.month,
                additionalstudentinfo__birth_date__day=today.day,
                classe__isnull=False,
            ).order_by("teaching")
            students = students.values_list(
                "last_name", "first_name", "classe__year", "classe__letter"
            )
            birthday += [
                {"name": "%s %s %s%s" % (s[0], s[1], s[2], s[3].upper())} for s in students
            ]
        elif people == "responsible":
            responsibles = ResponsibleModel.objects.filter(
                birth_date__month=today.month, birth_date__day=today.day, inactive_from__isnull=True
            )
            responsibles = responsibles.values_list("last_name", "first_name")
            birthday += [{"name": "%s %s" % (s[0], s[1])} for s in responsibles]
        return Response({"results": birthday})


class ScholarCalendarAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, format=None):
        start_year = get_scholar_year()
        start_month = get_core_settings().month_scholar_year_start
        start_day = get_core_settings().day_scholar_year_start
        cal = calendar.Calendar()
        day_of_week = {
            0: "Lu",
            1: "Ma",
            2: "Me",
            3: "Je",
            4: "Ve",
            5: "Sa",
            6: "Di",
        }
        dates = [
            (
                d[:3] + (day_of_week[d[3]], "")
                if d[2] >= start_day
                else d[:3] + (day_of_week[d[3]], "×")
            )
            for d in cal.itermonthdays4(start_year, start_month)
            if d[1] == start_month
        ]
        for m in range(start_month + 1, 13):
            dates += [
                d[:3] + (day_of_week[d[3]], "")
                for d in cal.itermonthdays4(start_year, m)
                if d[1] == m
            ]
        for m in range(1, start_month):
            dates += [
                d[:3] + (day_of_week[d[3]], "")
                for d in cal.itermonthdays4(start_year + 1, m)
                if d[1] == m
            ]
        dates += [
            (
                d[:3] + (day_of_week[d[3]], "")
                if d[2] < start_day
                else d[:3] + (day_of_week[d[3]], "×")
            )
            for d in cal.itermonthdays4(start_year + 1, start_month)
            if d[1] == start_month
        ]
        dates = [list(group) for key, group in itertools.groupby(dates, lambda d: d[1])]
        return Response(dates)


class CalendarAPI(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _today(event):
        now = timezone.now()
        if type(event["DTSTART"].dt) == date:
            return now.date()
        return now

    @staticmethod
    def _format_date(date, is_end=False):
        if ":" in str(date):
            print(date.strftime("%H:%M" if is_end else "%d/%m/%Y %H:%M"))
            return date.strftime("%H:%M" if is_end else "%d/%m/%Y %H:%M")
        else:
            if is_end:
                return (date - timedelta(days=1)).strftime("%d/%m/%Y")
            else:
                return date.strftime("%d/%m/%Y")

    # Cache for 6 hours.
    @method_decorator(cache_page(60 * 60 * 6))
    def get(self, format=None):
        events = []
        for cal_ics in ImportCalendarModel.objects.all():
            cal = Calendar.from_ical(requests.get(cal_ics.url).text)
            # for e in cal.walk('VEVENT'):
            #    if e['DTSTART'].dt > self._today(e) or e['DTSTART'].dt <= self._today(e) < e['DTEND'].dt:
            #        print(e['DTEND'].dt)
            evts = [
                {
                    "calendar": cal_ics.name,
                    "name": str(event["SUMMARY"]),
                    "begin": self._format_date(event["DTSTART"].dt),
                    "end": self._format_date(event["DTEND"].dt, True),
                }
                for event in cal.walk("VEVENT")
                if event["DTSTART"].dt > self._today(event)
                or event["DTSTART"].dt <= self._today(event) < event["DTEND"].dt
            ]
            events += evts
        events = sorted(events, key=lambda e: (e["begin"][6:], e["begin"][3:5], e["begin"][:2]))
        return Response({"results": events})


class PingAPI(APIView):
    def get(self, format=None):
        return Response(status=status.HTTP_200_OK, data={})


class BinaryFileRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = None
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        return data
