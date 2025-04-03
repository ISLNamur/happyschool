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

from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from django.contrib.auth.models import User

from .models import ScheduleChangeTypeModel
from .views import ScheduleChangeTypeViewSet


class TestScheduleChangeTypeViewSet(APITestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.dir_user = User.objects.get(username="director")
        self.view = ScheduleChangeTypeViewSet.as_view({"get": "list"})

    def test_get_change_type_list(self):
        request = self.factory.get("/api/schedule_change_type/")
        force_authenticate(request, user=self.dir_user)

        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 6)
