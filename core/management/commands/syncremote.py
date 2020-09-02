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

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from core.views import get_core_settings
from core.models import TeachingModel, ClasseModel, ResponsibleModel, StudentModel, CourseModel, GivenCourseModel
from core.serializers import TeachingSerializer, ClasseSerializer, ResponsibleRemoteSerializer, StudentWriteSerializer,\
    GroupSerializer, UserSerializer


class Command(BaseCommand):
    help = 'Sync core with a remote instance.'
    remote_url = ''
    header = {}

    def handle(self, *args, **options):
        settings = get_core_settings()
        if not settings.remote or not settings.remote_token:
            print("Settings for remote is not set in CoreSettings")

        self.remote_url = settings.remote
        if self.remote_url[-1] != '/':
            self.remote_url += '/'
        remote_token = settings.remote_token
        self.header = {'Authorization': 'Token %s' % remote_token}

        print("Teachings…")
        self.create_or_update_remote(TeachingModel, 'core/api/teaching', TeachingSerializer)
        print("Classes…")
        self.create_or_update_remote(ClasseModel, 'core/api/classe', ClasseSerializer)
        print("Groups…")
        self.create_or_update_remote(Group, 'core/api/group', GroupSerializer)
        print("Users…")
        self.create_or_update_remote(User, 'core/api/user', UserSerializer)
        print("Courses…")
        self.create_or_update_remote(CourseModel, "core/api/course")
        self.create_or_update_remote(GivenCourseModel, "core/api/given_course")
        print("Responsibles…")
        self.create_or_update_remote(ResponsibleModel, 'core/api/responsible', ResponsibleRemoteSerializer)
        print("Students…")
        self.create_or_update_remote(StudentModel, 'core/api/student', StudentWriteSerializer)

    def create_or_update_remote(self, model, base_url, serializer_class):
        import requests
        for obj in model.objects.all():
            url = self.remote_url + '%s/%i/' % (base_url, obj.pk,)
            result = requests.get(url, headers=self.header)
            print(result.status.code)
            serializer = serializer_class(obj)
            if result.status_code == 200:
                # Update data.
                update = requests.put(url, headers=self.header, json=serializer.data)
                print("Update %s: %s" % (str(obj), update.status_code == 200))
            elif result.status_code == 404:
                # Create data
                url = "/".join(url.split("/")[:-2]) + "/"
                create = requests.post(url, headers=self.header, json=serializer.data)
                print("Create %s: %s" % (str(obj), create.status_code == 201))
                if create.status_code != 201:
                    print(create.text)
