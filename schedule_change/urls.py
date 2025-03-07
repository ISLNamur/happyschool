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

app_name = "schedule_change"

urlpatterns = [
    path("", views.ScheduleChangeView.as_view(), name="schedule_change"),
    path(
        "fullscreen/",
        views.ScheduleChangeViewReadOnly.as_view(),
        name="fullscreen_schedule_change",
    ),
    path(
        "fullscreen_html/<str:show_for_students>/",
        views.FullscreenScheduleChangeView.as_view(),
        name="fullscreen_schedule_change_html",
    ),
    path("api/summary_pdf/", views.SummaryPDF.as_view()),
]

router = DefaultRouter()
router.register(r"api/schedule_change", views.ScheduleChangeViewSet)
router.register(r"api/schedule_change_type", views.ScheduleChangeTypeViewSet)
router.register(r"api/schedule_change_place", views.ScheduleChangePlaceViewSet)
router.register(r"api/schedule_change_category", views.ScheduleChangeCategoryViewSet)

urlpatterns += router.urls
