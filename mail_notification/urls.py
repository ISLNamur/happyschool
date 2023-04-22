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

app_name = "mail_notification"

urlpatterns = [
    path("", views.index, name="mail_notification"),
    path("list/", views.get_list, name="list"),
    path("emails_list/", views.EmailsList.as_view()),
    path("send_emails/", views.SendEmailsView.as_view(), name="send_emails"),
    path(
        "get_email_to_options/<teaching>/<to_type>/",
        views.get_email_to_options,
        name="get_email_to_options",
    ),
    path("get_tags_options/", views.get_tags_options, name="get_tags_options"),
    path("get_senders/<teaching>/", views.SendersList.as_view(), name="get_senders"),
    path("upload_file/", views.UploadFile.as_view(), name="attached_file"),
    path("upload_file/<int:pk>/", views.UploadFile.as_view(), name="remove_file"),
]

router = DefaultRouter()
router.register(r"api/other_email", views.OtherEmailViewSet)
router.register(r"api/other_email_group", views.OtherEmailGroupViewSet)
router.register(r"api/notif", views.EmailNotificationViewSet)

urlpatterns += router.urls
