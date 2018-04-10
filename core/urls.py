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

from . import views

app_name = 'core'

urlpatterns = [
    url(r'^profil$', views.profil, name='profil'),
    # url(r'^get_students_classes_years/(?P<teaching>\w+)/$', views.get_students_classes_years,
    #     name="get_students_classes_years"),
    # url(r'^get_students_classes_years/$', views.get_students_classes_years,
    #     name="get_students_classes_years"),
    # url(r'^get_teachers_by_name/(?P<teaching>\w+)/$', views.get_teachers_by_name,
    #     name="get_teachers_by_name"),
    # url(r'^get_teachers_by_name/$', views.get_teachers_by_name,
    #     name="get_teachers_by_name"),
    # url(r'^api/get_teachers_by_name/$', views.SearchTeachersView.as_view(), name='get_teachers_by_name'),
]
