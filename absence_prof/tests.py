from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.test.utils import override_settings


# Ensure we use the correct backend (ModelBackend)
@override_settings(AUTHENTICATION_BACKENDS=
                   ('django.contrib.auth.backends.ModelBackend',))
class AbsenceProfViewTest(TestCase):
    fixtures = ['motif_absence.json']

    def setUp(self):
        self.client = Client()

        # Create a superuser
        self.superuser = User.objects.create_user(username='testsuperuser', password='12345')
        self.superuser.is_staff = True
        self.superuser.is_admin = True
        self.superuser.is_superuser = True
        self.superuser.save()

        # Create a direction user
        self.dir_user = User.objects.create_user(username='director', password='67890')
        self.dir_user.is_active = True
        self.dir_user.save()

        # Create a student user
        self.student_user = User.objects.create_user(username='student', password='54321')
        self.student_user.is_active = True
        self.student_user.save()

        sysadmin_group = Group(name='sysadmin')
        sysadmin_group.save()
        sysadmin_group.user_set.add(self.superuser)

        direction_group = Group(name='direction')
        direction_group.save()
        direction_group.user_set.add(self.dir_user)

        student_group = Group(name='eleve')
        student_group.save()
        student_group.user_set.add(self.student_user)

        self.can_access_user = [{'username': 'testsuperuser', 'password': '12345'},
                                {'username': 'director', 'password': '67890'}]

    def check_page(self, page_url):
        # Test allowed users
        for user in self.can_access_user:
            self.client.login(username=user['username'], password=user['password'])
            response = self.client.get(page_url)
            self.assertEqual(response.status_code, 200)
            self.client.logout()

        # Student cannot access.
        self.client.login(username='student', password='54321')
        response = self.client.get(page_url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.get(page_url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/no_access/')
        self.client.logout()

        # Neither anonymous user
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 302)
        # Check if it is correctly redirected to auth
        response = self.client.get(page_url, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/auth')

    def test_index(self):
        self.check_page("/absences/")
