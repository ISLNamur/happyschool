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
from .adminsettings import views as admin_views


app_name = 'core'

urlpatterns = [
    url(r'^profil/$', views.ProfilView.as_view(), name='profil'),
    url(r'^members/$', views.MembersView.as_view(), name='members'),
    path('api/scholar_year/', views.ScholarYearAPI.as_view()),
    path('admin/', admin_views.AdminView.as_view()),
    path('api/testfile/', admin_views.TestFileAPIView.as_view()),
    path('api/import_students/', admin_views.ImportStudentAPIView.as_view()),
    path('api/birthday/', views.BirthdayAPI.as_view(), name='birthday'),
    path('api/calendar/', views.CalendarAPI.as_view(), name='calendar'),
    path('api/photo/', admin_views.PhotoAPI.as_view(), name='photo'),
    path('api/logo/', admin_views.LogoAPI.as_view(), name='logo'),
    path('api/update/', admin_views.UpdateAPIView.as_view(), name='update'),
    path('api/restart/', admin_views.RestartAPIView.as_view(), name='restart'),
    path('ping/', views.PingAPI.as_view(), name='ping'),
]

router = DefaultRouter()
router.register(r'api/members', views.MembersAPI)
router.register(r'api/teaching', views.TeachingViewSet)
router.register(r'api/email', views.EmailViewSet)
router.register(r'api/classe', views.ClasseViewSet)
router.register(r'api/responsible', views.ResponsibleViewSet)
router.register(r'api/student', views.StudentViewSet)

urlpatterns += router.urls
