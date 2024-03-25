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

from datetime import date

from django_weasyprint import WeasyTemplateView

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import ObjectDoesNotExist, query
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import DjangoModelPermissions

from django_filters import rest_framework as filters

from core.utilities import get_menu, get_scholar_year
from core.views import (
    BaseModelViewSet,
    get_app_settings,
    get_core_settings,
    BaseUploadFileView,
    LargePageSizePagination,
    BaseFilters,
)

from . import models
from . import serializers


def get_menu_entry(active_app: str, request) -> dict:
    if not request.user.has_perm("pia.view_piamodel"):
        return {}
    menu_entry = {"app": "pia", "display": "PIA", "url": "/pia", "active": active_app == "pia"}

    last_access = request.session.get("pia_last_access", None)
    if last_access:
        request.GET = request.GET.copy()
        request.GET["ordering"] = "-datetime_updated"
        view_set = PIAViewSet.as_view({"get": "list"})
        results = [c["id"] for c in view_set(request).data["results"]]
        menu_entry["new_items"] = models.PIAModel.objects.filter(
            id__in=results, datetime_updated__gt=last_access
        ).count()
        if menu_entry["new_items"] >= 20:
            menu_entry["new_items"] = "20+"

    return menu_entry


def get_settings():
    return get_app_settings(models.PIASettingsModel)


class PIAView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = "pia/pia.html"
    permission_required = ("pia.view_piamodel",)
    filters = [
        {"value": "student__display", "text": "Nom"},
        {"value": "student__matricule", "text": "Matricule"},
        {"value": "classe", "text": "Classe"},
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["menu"] = json.dumps(get_menu(self.request, "pia"))
        context["filters"] = json.dumps(self.filters)
        context["settings"] = json.dumps((serializers.PIASettingsSerializer(get_settings()).data))
        context["can_add_pia"] = json.dumps(self.request.user.has_perm("pia.add_piamodel"))

        dis_resp_cat = models.DisorderResponseCategoryModel.objects.all()
        dis_resp_cat_ser = serializers.DisorderResponseCategorySerializer(dis_resp_cat, many=True)
        context["disorder_response_category"] = json.dumps(dis_resp_cat_ser.data)

        context["disorder_responses"] = json.dumps(
            serializers.DisorderResponseSerializer(
                models.DisorderResponseModel.objects.all(), many=True
            ).data
        )

        context["pia_last_access"] = self.request.session.get("pia_last_access", "")
        # Set last access
        self.request.session["pia_last_access"] = timezone.now().isoformat()

        return context


class PIAFilterSet(BaseFilters):
    class Meta:
        fields_to_filter = ["student__matricule", "student__last_name", "advanced"]
        model = models.PIAModel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides


class PIAViewSet(BaseModelViewSet):
    queryset = models.PIAModel.objects.all()
    serializer_class = serializers.PIASerializer
    ordering_fields = (
        "student__classe__year",
        "student__classe__letter",
        "student__last_name",
        "datetime_updated",
    )
    filterset_class = PIAFilterSet

    username_field = None

    def is_only_tenure(self):
        return get_settings().filter_teacher_entries_by_tenure

    def get_group_all_access(self):
        return get_settings().all_access.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        create_log = models.LogPIAModel(
            log=f"PIA from {str(instance.student)} is created by {self.request.user.username}"
        )
        create_log.save()

    def perform_destroy(self, instance):
        delete_log = models.LogPIAModel(
            log=f"PIA from {str(instance.student)} is deleted by {self.request.user.username}"
        )
        delete_log.save()
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        update_log = models.LogPIAModel(
            log=f"PIA from {str(instance.student)} is updated by {self.request.user.username}"
        )
        update_log.save()


class BaseGoalFilters(filters.FilterSet):
    current_scholar_year = filters.BooleanFilter(method="current_scholar_year_by")

    def current_scholar_year_by(self, queryset, name, value):
        if not value:
            return queryset

        core_settings = get_core_settings()
        date_start = f"{get_scholar_year()}-{core_settings.month_scholar_year_start}-{core_settings.day_scholar_year_start}"

        return queryset.filter(date_start__gte=date_start)


class CrossGoalFilters(BaseGoalFilters):
    class Meta:
        model = models.CrossGoalModel
        fields = ["pia_model", "current_scholar_year"]


class CrossGoalViewSet(ModelViewSet):
    queryset = models.CrossGoalModel.objects.all()
    serializer_class = serializers.CrossGoalSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = CrossGoalFilters
    ordering_fields = ["date_start", "date_end", "datetime_creation"]
    ordering = [
        "-date_end",
        "-date_start",
    ]
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class BranchGoalFilters(BaseGoalFilters):
    class Meta:
        model = models.BranchGoalModel
        fields = ["pia_model", "current_scholar_year", "branch"]


class BranchGoalViewSet(ModelViewSet):
    queryset = models.BranchGoalModel.objects.all()
    serializer_class = serializers.BranchGoalSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = BranchGoalFilters
    ordering_fields = ["datetime_creation"]
    ordering = [
        "-date_end",
        "-date_start",
    ]
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class IntermediateEvaluationViewSet(ModelViewSet):
    queryset = models.IntermediateEvaluationModel.objects.all()
    serializer_class = serializers.IntermediateEvaluationSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("branch_goal",)
    ordering_fields = ["date_evaluation"]
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class OtherStatementViewSet(ModelViewSet):
    queryset = models.OtherStatementModel.objects.all()
    serializer_class = serializers.OtherStatementSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("class_council",)
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class ClassCouncilPIAViewSet(ModelViewSet):
    queryset = models.ClassCouncilPIAModel.objects.all()
    serializer_class = serializers.ClassCouncilPIASerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("pia_model",)
    ordering = ["-datetime_creation", "-date_council"]
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class DisorderViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderModel.objects.all()
    serializer_class = serializers.DisorderSerializer
    pagination_class = LargePageSizePagination


class DisorderResponseViewSet(ReadOnlyModelViewSet):
    queryset = models.DisorderResponseModel.objects.all()
    serializer_class = serializers.DisorderResponseSerializer
    pagination_class = LargePageSizePagination


class SelectedDisorderResponseViewSet(ModelViewSet):
    queryset = models.SelectedDisorderResponseModel.objects.all()
    serializer_class = serializers.SelectedDisorderResponseSerializer
    pagination_class = LargePageSizePagination


class SelectedDisorderResponseNewViewSet(ModelViewSet):
    queryset = models.SelectedDisorderResponseNewModel.objects.all()
    serializer_class = serializers.SelectedDisorderResponseNewSerializer
    pagination_class = LargePageSizePagination

    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    filterset_fields = ("disorder_care",)


class DisorderCareViewSet(ModelViewSet):
    queryset = models.DisorderCareModel.objects.all()
    serializer_class = serializers.DisorderCareSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-date_start"]


class OtherAdjustmentsViewSet(ModelViewSet):
    queryset = models.OtherAdjustmentsModel.objects.all()
    serializer_class = serializers.OtherAdjustmentsSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-date_start"]


class ScheduleAdjustmentViewSet(ReadOnlyModelViewSet):
    """Read only view set for schedule adjustment model."""

    queryset = models.ScheduleAdjustmentModel.objects.all()
    serializer_class = serializers.ScheduleAdjustmentSerializer
    pagination_class = LargePageSizePagination


class ScheduleAdjustmentPlanViewSet(ModelViewSet):
    queryset = models.ScheduleAdjustmentPlanModel.objects.all()
    serializer_class = serializers.ScheduleAdjustmentPlanSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-date_start"]


class ActivitySupportViewSet(ModelViewSet):
    queryset = models.ActivitySupportModel.objects.all()
    serializer_class = serializers.ActivitySupportSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-date_start"]


class CourseReinforcementViewSet(ModelViewSet):
    queryset = models.CourseReinforcementModel.objects.all()
    serializer_class = serializers.CourseReinforcementSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-date_start"]


class CrossGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.CrossGoalItemModel.objects.all()
    serializer_class = serializers.CrossGoalItemSerializer
    pagination_class = LargePageSizePagination


class AssessmentViewSet(ReadOnlyModelViewSet):
    queryset = models.AssessmentModel.objects.all()
    serializer_class = serializers.AssessmentSerializer
    pagination_class = LargePageSizePagination


class BranchViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchModel.objects.all()
    serializer_class = serializers.BranchSerializer
    pagination_class = LargePageSizePagination


class BranchGoalItemViewSet(ReadOnlyModelViewSet):
    queryset = models.BranchGoalItemModel.objects.all()
    serializer_class = serializers.BranchGoalItemSerializer
    pagination_class = LargePageSizePagination


class UploadFileView(BaseUploadFileView):
    file_model = models.AttachmentModel
    file_serializer = serializers.AttachmentSerializer


class StudentProjectViewSet(ModelViewSet):
    queryset = models.StudentProjectModel.objects.all()
    serializer_class = serializers.StudentProjectSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-datetime_creation"]
    permission_classes = (DjangoModelPermissions,)


class ParentsOpinionViewSet(ModelViewSet):
    queryset = models.ParentsOpinionModel.objects.all()
    serializer_class = serializers.ParentsOpinionSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("pia_model",)
    pagination_class = LargePageSizePagination
    ordering = ["-datetime_creation"]
    permission_classes = (DjangoModelPermissions,)


class StudentStateViewSet(ModelViewSet):
    queryset = models.StudentStateModel.objects.all()
    serializer_class = serializers.StudentStateSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields = ("class_council",)
    pagination_class = LargePageSizePagination
    permission_classes = (DjangoModelPermissions,)


class ResourceDifficultyViewSet(ReadOnlyModelViewSet):
    queryset = models.ResourceDifficultyModel.objects.all()
    serializer_class = serializers.ResourceDifficultySerializer
    pagination_class = LargePageSizePagination


class ReportPDFView(LoginRequiredMixin, PermissionRequiredMixin, WeasyTemplateView):
    permission_required = "pia.view_piamodel"

    template_name = "pia/report.html"
    day_of_week = {
        1: "Lundi",
        2: "Mardi",
        3: "Mercredi",
        4: "Jeudi",
        5: "Vendredi",
        6: "Samedi",
        7: "Dimanche",
    }

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        filter_date_from = ""
        if "current_year" in kwargs and kwargs["current_year"]:
            year = get_scholar_year()
            month = get_core_settings().month_scholar_year_start
            day = get_core_settings().day_scholar_year_start
            filter_date_from = f"{year}-{month:02d}-{day:02d}"

        context["date_filter"] = filter_date_from

        try:
            context["pia"] = models.PIAModel.objects.get(id=int(kwargs["pia"]))
            context["disorder_response_categories"] = (
                models.DisorderResponseCategoryModel.objects.all()
            )

            context["support_activities"] = [
                {
                    "activities": [
                        {
                            "day": self.day_of_week[int(s_a[0])],
                            "branch": " ".join([b["branch"] for b in s_a[1]["branch"]]),
                            "teachers": ", ".join(
                                [f"{t['first_name']} {t['last_name']}" for t in s_a[1]["teachers"]]
                            ),
                        }
                        for s_a in activity_support.support_activities.items()
                    ],
                    "directed_study": ", ".join(
                        [
                            self.day_of_week[int(d_s_day)]
                            for d_s_day in activity_support.directed_study["days"]
                        ]
                    ),
                    "object": activity_support,
                }
                for activity_support in context["pia"].activitysupportmodel_set.all()
            ]
        except ObjectDoesNotExist:
            pass
        return context
