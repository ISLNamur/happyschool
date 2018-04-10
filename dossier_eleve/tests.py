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

# from django.utils import timezone
#
# from django.contrib.auth.models import User, Group
# from django.test import TestCase, Client
# from django.test.utils import override_settings
#
# from core.models import StudentModel
#
# from .models import InfoEleve, SanctionDecisionDisciplinaire, CasEleve
#
# # Ensure we use the correct backend (ModelBackend)
# @override_settings(AUTHENTICATION_BACKENDS=
#                    ('django.contrib.auth.backends.ModelBackend',))
# class DossierEleveViewTest(TestCase):
#     fixtures = ['dossier_eleve_infos.json', 'dossier_eleve_sanctions.json']
#
#     def setUp(self):
#         self.client = Client()
#
#         # Create a superuser
#         self.superuser = User.objects.create_user(username='testsuperuser', password='12345')
#         self.superuser.is_staff = True
#         self.superuser.is_admin = True
#         self.superuser.is_superuser = True
#         self.superuser.save()
#
#         # Create a direction user
#         self.dir_user = User.objects.create_user(username='director', password='67890')
#         self.dir_user.is_active = True
#         self.dir_user.save()
#
#         # Create a student user
#         self.student_user = User.objects.create_user(username='student', password='54321')
#         self.student_user.is_active = True
#         self.student_user.save()
#
#         sysadmin_group = Group(name='sysadmin')
#         sysadmin_group.save()
#         sysadmin_group.user_set.add(self.superuser)
#
#         direction_group = Group(name='direction')
#         direction_group.save()
#         direction_group.user_set.add(self.dir_user)
#
#         student_group = Group(name='eleve')
#         student_group.save()
#         student_group.user_set.add(self.student_user)
#
#         # Create a student
#         StudentModel(1, 'Totoé', 'Totoe', 'Ohé', 'Ohe', '1c', 1, 'secondaire').save()
#
#         self.can_access_user = [{'username': 'testsuperuser', 'password': '12345'},
#                            {'username': 'director', 'password': '67890'}]
#
#     def check_page(self, page_url):
#         # Test allowed users
#         for user in self.can_access_user:
#             self.client.login(username=user['username'], password=user['password'])
#             response = self.client.get(page_url)
#             self.assertEqual(response.status_code, 200)
#             self.client.logout()
#
#         # Student cannot access.
#         self.client.login(username='student', password='54321')
#         response = self.client.get(page_url)
#         self.assertNotEqual(response.status_code, 200)
#         response = self.client.get(page_url, follow=True)
#         self.assertEqual(response.request['PATH_INFO'], '/no_access/')
#         self.client.logout()
#
#         # Neither anonymous user
#         response = self.client.get(page_url)
#         self.assertEqual(response.status_code, 302)
#         # Check if it is correctly redirected to auth
#         response = self.client.get(page_url, follow=True)
#         self.assertEqual(response.request['PATH_INFO'], '/auth')
#
#     def test_index(self):
#         self.check_page("/dossier_eleve/")
#
#     def test_get_cas(self):
#         # Empty cas list
#         self.check_page("/dossier_eleve/get_cas/")
#
#         # Add cas
#         student = StudentModel.objects.all()[0]
#         CasEleve(matricule=student,
#                  name='Toto',
#                  datetime_encodage=timezone.now(),
#                  info=InfoEleve.objects.all()[0],
#                  demandeur='Mechant',
#                  sanction_decision=None,
#                  explication_commentaire='Parce que',
#                  datetime_sanction=None,
#                  datetime_conseil=None,
#                  sanction_faite=None,
#                  important=False,
#                  ).save()
#         CasEleve(matricule=student,
#                  name='Toto',
#                  datetime_encodage=timezone.now(),
#                  info=None,
#                  demandeur='Zorro',
#                  sanction_decision=SanctionDecisionDisciplinaire.objects.all()[0],
#                  explication_commentaire='La',
#                  datetime_sanction=timezone.now(),
#                  datetime_conseil=timezone.now(),
#                  sanction_faite=False,
#                  important=False,
#                  ).save()
#
#         for user in self.can_access_user:
#             self.client.login(username=user['username'], password=user['password'])
#             response = self.client.get("/dossier_eleve/get_cas/")
#
#             self.assertEqual(response.status_code, 200)
#             # Should find the two entries
#             self.assertEquals(len(str(response.content).split("<tr")) - 2, 2)
#
#             # Get only actives. Should find one entry
#             response = self.client.get("/dossier_eleve/get_cas/", {'active': "1"})
#             self.assertEquals(len(str(response.content).split("<tr")) - 2, 1)
#             self.client.logout()
#
#     def test_get_nouveau_cas(self):
#         self.check_page("/dossier_eleve/nouveau_cas/")
#
#     def test_get_pdf(self):
#         self.client.login(username='testsuperuser', password='12345')
#         response = self.client.get("/dossier_eleve/get_pdf/1/1/")
#         self.assertEqual(response.status_code, 200)
#
#         # # Add cas
#         # student = StudentLDAP.objects.all()[0]
#         # CasEleve(matricule=student,
#         #          name='Toto',
#         #          datetime_encodage=timezone.now(),
#         #          info=InfoEleve.objects.all()[0],
#         #          demandeur='Mechant',
#         #          sanction_decision=None,
#         #          explication_commentaire='Parce que',
#         #          datetime_sanction=None,
#         #          datetime_conseil=None,
#         #          sanction_faite=None,
#         #          important=False,
#         #          ).save()
#         # CasEleve(matricule=student,
#         #          name='Toto',
#         #          datetime_encodage=timezone.now(),
#         #          info=None,
#         #          demandeur='Zorro',
#         #          sanction_decision=SanctionDecisionDisciplinaire.objects.all()[0],
#         #          explication_commentaire='La',
#         #          datetime_sanction=timezone.now(),
#         #          datetime_conseil=timezone.now(),
#         #          sanction_faite=False,
#         #          important=False,
#         #          ).save()
#         #
#         # response = self.client.get("/dossier_eleve/get_pdf/1/1/")
#         # print(response)
#
#
