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
from annuaire.views import SearchPeopleAPI

app_name = 'student_absence'

urlpatterns = [
    path('', views.StudentAbsenceView.as_view(), name="student_absence"),
    path('api/absence_count/', views.AbsenceCountAPI.as_view(), name="absence_count"),
    path('api/students_classes/', SearchPeopleAPI.as_view()),
]

router = DefaultRouter()
router.register(r'api/student_absence', views.StudentAbsenceViewSet)
router.register(r'api/justification', views.JustificationViewSet)
router.register(r'api/classenote', views.ClasseNoteViewSet)
router.register(r'api/period', views.PeriodViewSet)

urlpatterns += router.urls

if "proeco" in settings.INSTALLED_APPS:
    urlpatterns.append(path('api/export_selection/', views.ExportStudentAbsenceAPI.as_view()))
