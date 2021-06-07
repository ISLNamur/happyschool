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

import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group, User


class PyramidVisibilityTests(APITestCase):
    fixtures = ["test_dossier_eleve_users.json", "test_dossier_eleve_settings_pyramid.json"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username='director')
        # Get a student user.
        self.student_user = User.objects.get(username='student')
        # Get a teacher user.
        self.teacher_user = User.objects.get(username='teacher')
        # Get an educator user.
        self.educator_user = User.objects.get(username='educator')
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username='coordonator')
        # Get a sysadmin user.
        self.admin_user = User.objects.get(username='admin')

        self.coordonator_group = Group.objects.get(name="coordonateur")
        self.educator_group = Group.objects.get(name="educateur")
        self.director_group = Group.objects.get(name="direction")
        self.teacher_group = Group.objects.get(name="professeur")

    def _create_cas_and_test_visibility(
        self, creator, users_success, users_failure, visible_by_group_id, visible_by_tenure=False,
    ):
        self.client.force_authenticate(user=creator)
        url = "/dossier_eleve/api/cas_eleve/"
        data = {
            "name": "Tutu Toto",
            "matricule_id": 1234,
            "info_id": 6,
            "sanction_decision_id": None,
            "explication_commentaire": "<p>Test</p>",
            "important": False,
            "demandeur": "Sible Trespon",
            "visible_by_groups": visible_by_group_id,
            "datetime_sanction": None,
            "sanction_faite": None,
            "send_to_teachers": False,
            "attachments": [],
            "visible_by_tenure": visible_by_tenure
        }
        response = self.client.post(url, data, format='json')
        post_response = response
        # It should respond successfully.
        self.assertEqual(response.status_code, 201)
        cas_id = response.data["id"]

        response = self.client.get(f"{url}{cas_id}/")
        self.assertEqual(response.data["matricule_id"], 1234)
        self.assertEqual(response.data["explication_commentaire"], "<p>Test</p>")

        # Test access with other users that should fail.
        for u in users_failure:
            self.client.force_authenticate(user=u)
            response = self.client.get(f"{url}{cas_id}/")
            self.assertEqual(response.status_code, 404)

        # Test access with other users that should succed.
        for u in users_success:
            self.client.force_authenticate(user=u)
            response = self.client.get(f"{url}{cas_id}/")
            self.assertEqual(response.status_code, 200)

        return post_response

    def test_creation_and_forced_visibility(self):
        """
        Create a cas and test forced visibility by other groups and itself.
        """
        # Test visibility from a director's cas without setting visibility (test forced visibility).
        response = self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user],
            [self.student_user, self.coordonator_user, self.teacher_user, self.educator_user],
            [],
            False
        )
        self.assertEqual(response.data["visible_by_tenure"], False)

        # # Test visibility from a coordonator's cas without setting visibility (test forced visibility).
        response = self._create_cas_and_test_visibility(
            self.coordonator_user,
            [self.admin_user, self.dir_user, self.coordonator_user],
            [self.student_user, self.teacher_user, self.educator_user],
            [],
            False
        )
        self.assertEqual(response.data["visible_by_tenure"], False)

        # # Test visibility from a educator's cas without setting visibility (test forced visibility).
        response = self._create_cas_and_test_visibility(
            self.educator_user,
            [self.admin_user, self.dir_user, self.coordonator_user, self.educator_user],
            [self.student_user, self.teacher_user],
            [],
        )

        self.assertEqual(response.data["visible_by_tenure"], False)

        # Test visibility from a teacher's cas without setting visibility (test forced visibility).
        response = self._create_cas_and_test_visibility(
            self.teacher_user,
            [self.admin_user, self.dir_user, self.coordonator_user, self.teacher_user, self.teacher_user],
            [self.student_user],
            []
        )

        self.assertEqual(response.data["visible_by_tenure"], True)

    def test_creation_and_visibility_setting(self):
        """
        Create a cas and test setting visibility for other groups.
        """
        #Test visibility from a director's cas with visibility to coordonators.
        self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user, self.coordonator_user],
            [self.student_user, self.teacher_user, self.educator_user],
            [self.coordonator_group.id]
        )

        # Test visibility from a director's cas with visibility to educators.
        self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user, self.educator_user],
            [self.student_user, self.teacher_user, self.coordonator_user],
            [self.educator_group.id]
        )

        # Test visibility from a director's cas with visibility to teachers.
        self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user, self.teacher_user],
            [self.student_user, self.educator_user, self.coordonator_user],
            [self.teacher_group.id]
        )

        # Test visibility from a director's cas with visibility to all.
        self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user, self.teacher_user, self.coordonator_user, self.educator_user],
            [self.student_user],
            [self.teacher_group.id, self.educator_group.id, self.coordonator_group.id]
        )

        # Test tenure visibility (coordonator is the tenure).
        self._create_cas_and_test_visibility(
            self.dir_user,
            [self.admin_user, self.dir_user, self.coordonator_user],
            [self.student_user, self.teacher_user, self.educator_user],
            [],
            True
        )
