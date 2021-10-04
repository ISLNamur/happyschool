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

urlpatterns = [
    path("", views.LatenessView.as_view(), name="lateness"),
]

router = DefaultRouter()
router.register(r"api/lateness", views.LatenessViewSet)
router.register(r"api/settings", views.LatenessSettingsViewSet)
urlpatterns += router.urls

if "proeco" in settings.INSTALLED_APPS:
    urlpatterns.append(path("proeco_list/<part_of_day>/", views.ExportStudentToProEco.as_view()))
