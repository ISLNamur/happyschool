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

from django.conf.urls import url

from . import views

app_name = 'mail_notification'

urlpatterns = [
    url(r'^$', views.index, name='mail_notification'),
    url(r'^list/$', views.get_list, name='list'),
    url(r'^emails_list/$', views.EmailsList.as_view()),
    url(r'^send_emails/$', views.SendEmailsView.as_view(), name='send_emails'),
    url(r'^get_email_to_options/(?P<teaching>\w+)/(?P<to_type>\w+)/$', views.get_email_to_options, name='get_email_to_options'),
    url(r'^get_tags_options/$', views.get_tags_options, name='get_tags_options'),
    url(r'^get_senders/(?P<teaching>\w+)/', views.SendersList.as_view(), name='get_senders'),
    url(r'^upload_file/$', views.UploadFile.as_view(), name='attached_file'),
    url(r'^upload_file/(?P<pk>[0-9]+)/$', views.UploadFile.as_view(), name='remove_file'),
]

router = DefaultRouter()
router.register(r'api/other_email', views.OtherEmailViewSet)
router.register(r'api/other_email_group', views.OtherEmailGroupViewSet)

urlpatterns += router.urls
