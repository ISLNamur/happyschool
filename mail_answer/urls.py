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

from rest_framework.routers import DefaultRouter

from django.urls import path

from . import views

app_name = "mail_answer"

urlpatterns = [
    path("", views.MailAnswerView.as_view(), name="mail_answer"),
    path("answer/<uuid:answer>/", views.AnswerView.as_view(), name="answer"),
    path("api/answers/<int:template>/<int:classe>/", views.AnswersAPI.as_view(), name="answers"),
    path(
        "api/answers_classes/<int:template>/",
        views.AnswersClassesAPI.as_view(),
        name="answers_classes",
    ),
]

router = DefaultRouter()
router.register(r"api/choices", views.ChoicesViewSet)
router.register(r"api/options", views.OptionsViewSet)
router.register(r"api/mail_template", views.MailTemplateViewSet)
router.register(r"api/mail_answer", views.MailAnswerViewSet)
router.register(r"api/public/mail_answer", views.MailAnswerUpdateViewSet, "public-mail-answer")

urlpatterns += router.urls
