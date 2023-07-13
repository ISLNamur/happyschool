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


from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

app_name = "pia"

urlpatterns = [
    path("", views.PIAView.as_view(), name="pia"),
    path("report/<int:pia>/", views.ReportPDFView.as_view()),
    path("upload_file/", views.UploadFileView.as_view()),
    path("upload_file/<int:pk>/", views.UploadFileView.as_view()),
]

router = DefaultRouter()
router.register(r"api/pia", views.PIAViewSet)
router.register(r"api/disorder", views.DisorderViewSet)
router.register(r"api/disorder_response", views.DisorderResponseViewSet)
router.register(r"api/selected_disorder_response", views.SelectedDisorderResponseViewSet)
router.register(r"api/selected_disorder_response_new", views.SelectedDisorderResponseNewViewSet)
router.register(r"api/disorder_care", views.DisorderCareViewSet)
router.register(r"api/schedule_adjustment", views.ScheduleAdjustmentViewSet)
router.register(r"api/cross_goal", views.CrossGoalViewSet)
router.register(r"api/assessment", views.AssessmentViewSet)
router.register(r"api/branch", views.BranchViewSet)
router.register(r"api/branch_goal", views.BranchGoalViewSet)
router.register(r"api/cross_goal_item", views.CrossGoalItemViewSet)
router.register(r"api/branch_goal_item", views.BranchGoalItemViewSet)
router.register(r"api/class_council", views.ClassCouncilPIAViewSet)
router.register(r"api/other_statement", views.OtherStatementViewSet)
router.register(r"api/student_project", views.StudentProjectViewSet)
router.register(r"api/parents_opinion", views.ParentsOpinionViewSet)
router.register(r"api/resource_difficulty", views.ResourceDifficultyViewSet)
router.register(r"api/council_statement", views.StudentStateViewSet)

urlpatterns += router.urls
