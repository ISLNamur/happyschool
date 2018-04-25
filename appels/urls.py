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

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    url(r'^$', views.index, name='appels'),
    url(r'^get_appels$', views.get_appels, name='get_appels'),
    url(r'^nouvel_appel$', views.nouvel_appel, name='nouvel_appel'),
    url(r'^traiter_appel/(?P<appelId>[0-9]+)$', views.traiter_appel, name='traiter_appel'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
    url(r'vue', views.test_vue, name='test_vue'),
]

router = DefaultRouter()
router.register(r'api/appel', views.AppelViewSet)
router.register(r'api/motive', views.MotiveViewSet)
router.register(r'api/object', views.ObjectViewSet)

urlpatterns += router.urls