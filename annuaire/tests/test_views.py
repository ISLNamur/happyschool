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

from django.contrib.auth.models import User
from django.test import Client, TestCase


class ClassListPDFTest(TestCase):
    fixtures = ["test_core.json"]

    def setUp(self):
        self.client = Client()

        self.teacher_user = User.objects.get(username="teacher")
        self.client.force_login(user=self.teacher_user)

    def test_pdf_generation(self):
        """
        Ensure pdf can be generated
        """
        url = "/annuaire/get_class_list_pdf/1/"

        response = self.client.get(url)
        # It should happily respond.
        self.assertEqual(response.status_code, 200)
        # The content should truly exists.
        self.assertGreater(len(response.content), 1000)
