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
from django.conf import settings

from rest_framework.routers import DefaultRouter

from . import views

app_name = "student_absence_teacher"

urlpatterns = [
    path("", views.StudentAbsenceTeacherView.as_view(), name="student_absence_teacher"),
    path("export/<document>/<date_from>/<date_to>/", views.ExportAbsencesAPI.as_view()),
    path("api/count_absence/<date>/<point_of_view>/<class_list>/", views.OverviewAPI.as_view()),
    path("api/count_no_justification/<student>/", views.NoJustificationCountAPI.as_view()),
    path("api/count_justification/<student>/", views.JustificationCountAPI.as_view()),
    path("api/mail_warning_template/<student_id>/<date_start>/<date_end>/", views.MailWarningTemplateAPI.as_view()),
    path("api/mail_warning/", views.MailWarningAPI.as_view()),
    path("get_pdf_warning/", views.WarningPDF.as_view()),
    path("api/exclude_student/", views.ExcludeStudentAPI.as_view()),
]

router = DefaultRouter()
router.register(r"api/period_teacher", views.PeriodTeacherViewSet)
router.register(r"api/period_educ", views.PeriodEducViewSet)
router.register(r"api/absence_teacher", views.StudentAbsenceTeacherViewSet)
router.register(r"api/absence_educ", views.StudentAbsenceEducViewSet)
router.register(r"api/justification", views.JustificationViewSet)
router.register(r"api/just_motive", views.JustMotiveViewSet)

urlpatterns += router.urls

if "proeco" in settings.INSTALLED_APPS:
    urlpatterns.append(path("api/export_selection/", views.ExportStudentAbsenceAPI.as_view()))
