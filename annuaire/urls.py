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

urlpatterns = [
    path("get_class_photo_pdf/", views.ClassePhotosView.as_view()),
    path("", views.AnnuaireView.as_view(), name="annuaire"),
    path("get_class_list_excel/", views.ClasseListExcelView.as_view()),
    path("get_class_list_pdf/<int:classe_id>/", views.ClasseListPDF.as_view()),
    path("api/people/", views.SearchPeopleAPI.as_view()),
    path("api/classes/", views.SearchClassesAPI.as_view()),
    path("api/people_or_classes/", views.SearchClassesOrPeopleAPI.as_view()),
    path("api/studentclasse/", views.StudentClasseAPI.as_view()),
    path("api/student_given_course/<int:given_course_id>/", views.StudentGivenCourseAPI.as_view()),
    path("api/course_to_classes/<int:given_course_id>/", views.CourseToClassesAPI.as_view()),
    path(
        "summary/<str:category>/<int:id>/<str:date_from>/<str:date_to>/",
        views.SummaryPDF.as_view(),
        name="summary",
    ),
    path("api/yellowpage/<str:phonenum>/", views.YellowpageAPI.as_view()),
    path("api/emailsearcher/<str:email>/", views.EmailSearcherAPI.as_view()),
]

router = DefaultRouter()
router.register(r"api/settings", views.AnnuaireSettingsViewSet)
router.register(r"api/student", views.StudentInfoViewSet)
router.register(r"api/responsible", views.ResponsibleInfoViewSet)
router.register(
    r"api/responsible_sensitive", views.ResponsibleSensitiveViewSet, "responsible-sensitive"
)
router.register(r"api/student_sensitive", views.StudentSensitiveInfoViewSet, "student-sensitive")
router.register(r"api/info_general", views.StudentGeneralInfoViewSet, "info-general")
router.register(r"api/info_contact", views.StudentContactInfoViewSet, "info-contact")
router.register(r"api/info_medical", views.StudentMedicalInfoViewSet, "info-medical")

urlpatterns += router.urls
