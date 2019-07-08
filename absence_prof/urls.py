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

app_name = 'absence_prof'

urlpatterns = [
    path('list/', views.ListPDF.as_view()),
    path('', views.AbsenceProfView.as_view(), name="index"),
]

router = DefaultRouter()
router.register(r'api/absence', views.AbsenceProfViewSet)
router.register(r'api/motif', views.MotifAbsenceViewSet)

urlpatterns += router.urls
