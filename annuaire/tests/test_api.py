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

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class AccountTests(APITestCase):
    fixtures = ["test_core.json"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username="director")
        # Get a student user.
        self.student_user = User.objects.get(username="student")
        # Get a teacher user.
        self.teacher_user = User.objects.get(username="teacher")
        # Get an educator user.
        self.educator_user = User.objects.get(username="educator")
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username="coordonator")

    def test_search_people(self):
        """
        Ensure we can search and find someone.
        """
        url = "/annuaire/api/people/"
        data = {
            "query": "tut",
        }
        response = self.client.post(url, data, format="json")
        # Without authentification, it should fail wih unauthorized.
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.dir_user)
        response = self.client.post(url, data, format="json")
        # It should respond successfully.
        self.assertEqual(response.status_code, 200)
        # It should have several responses.
        self.assertGreater(len(response.data), 0)
