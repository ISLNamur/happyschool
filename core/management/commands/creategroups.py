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

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create groups in database based on settings.py.'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name=settings.SYSADMIN_GROUP)
        Group.objects.get_or_create(name=settings.DIRECTION_GROUP)
        Group.objects.get_or_create(name=settings.TEACHER_GROUP)
        Group.objects.get_or_create(name=settings.EDUCATOR_GROUP)
        Group.objects.get_or_create(name=settings.COORDONATOR_GROUP)
        Group.objects.get_or_create(name=settings.SECRETARY_GROUP)
        Group.objects.get_or_create(name=settings.PMS_GROUP)
        Group.objects.get_or_create(name=settings.RECEPTION_GROUP)
        for i in range(1, 8):
            Group.objects.get_or_create(name=settings.COORD_GROUP + str(i))
            Group.objects.get_or_create(name=settings.EDUC_GROUP + str(i))
