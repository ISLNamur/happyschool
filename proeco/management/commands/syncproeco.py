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

from datetime import date

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import TeachingModel
from core.adminsettings.importclass import ImportStudentFDB, ImportResponsibleFDB


class Command(BaseCommand):
    help = 'Sync django database with a ProEco database.'

    def handle(self, *args, **options):

        proecos = settings.SYNC_FDB_SERVER
        for proeco in proecos:
            teaching = TeachingModel.objects.get(name=proeco["teaching_name"])
            classe_format = proeco["classe_format"] if "classe_format" in proeco else "%C"
            username_attribute = proeco["username_attribute"] if "username_attribute" in proeco else None
            importation_student = ImportStudentFDB(teaching=teaching, fdb_server=proeco["server"],
                                                   teaching_type=proeco["teaching_type"],
                                                   search_login_directory=settings.USE_LDAP_INFO,
                                                   classe_format=classe_format)
            importation_responsible = ImportResponsibleFDB(teaching=teaching, fdb_server=proeco["server"],
                                                           teaching_type=proeco["teaching_type"],
                                                           search_login_directory=settings.USE_LDAP_INFO,
                                                           ldap_unique_attr=proeco["ldap_unique_attr"]["teacher_ldap_attr"],
                                                           classe_format=classe_format,
                                                           username_attribute=username_attribute)
            importation_student.sync()
            importation_responsible.sync()
