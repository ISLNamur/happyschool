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

from django.conf.urls import url
from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^get_list/$', views.get_list, name='get_list'),
    url(r'^get_people_names/(?P<enseignement>\w+)/(?P<people_type>\w+)/(?P<check_access>[0-9]+)/$', views.get_people_names,
        name='get_people_names'),
    url(r'^get_people_names/(?P<enseignement>\w+)/(?P<people_type>\w+)/$', views.get_people_names,
        name='get_people_names'),
    url(r'^get_people_names/$', views.get_people_names, name='get_people_names'),
    url(r'^get_students_matricules/', views.get_students_matricules, name='get_students_matricules'),
    url(r'^get_students_or_classes/(?P<enseignement>\w+)/(?P<check_access>[0-9]+)/$', views.get_students_or_classes,
        name='get_students_or_classes'),
    url(r'^get_students_or_classes/', views.get_students_or_classes, name='get_students_or_classes'),
    url(r'^get_teachers_emails/', views.get_teachers_emails, name='get_teachers_emails'),
    url(r'^student/(?P<matricule>[0-9]+)/info/(?P<medical_info>\w+)/(?P<user_info>\w+)', views.info, name='info'),
    url(r'^student/(?P<matricule>[0-9]+)/info', views.info, name='info'),
    url(r'^student/(?P<matricule>[0-9]+)/', views.summary, name='summary'),
    url(r'^teacher/(?P<matricule>[0-9]+)/info/$', views.info_teacher, name='info_teacher'),
    url(r'^teacher/(?P<id>[0-9]+)/$', views.summary_teacher, name='summary_teacher'),
    url(r'^get_class_photo_pdf/(?P<year>[0-9]+)/(?P<classe>\w+)/(?P<enseignement>\w+)/$', views.get_class_photo_pdf,
        name="get_class_photo_pdf"),
    path('', views.AnnuaireView.as_view(), name='annuaire'),
    path('get_class_list_excel/<int:classe_id>/', views.ClasseListExcelView.as_view()),
    path('get_class_list_pdf/<int:classe_id>/', views.ClasseListPDFView.as_view()),
    path('api/people/', views.SearchPeopleAPI.as_view()),
    path('api/classes/', views.SearchClassesAPI.as_view()),
    path('api/people_or_classes/', views.SearchClassesOrPeopleAPI.as_view()),
    path('api/studentclasse/', views.StudentClasseAPI.as_view()),
]

router = DefaultRouter()
router.register(r'api/student', views.StudentInfoViewSet)
router.register(r'api/responsible', views.ResponsibleInfoViewSet)
router.register(r'api/responsible_sensitive', views.ResponsibleSensitiveViewSet)
router.register(r'api/info_general', views.StudentGeneralInfoViewSet)
router.register(r'api/info_contact', views.StudentContactInfoViewSet)
router.register(r'api/info_medical', views.StudentMedicalInfoViewSet)

urlpatterns += router.urls