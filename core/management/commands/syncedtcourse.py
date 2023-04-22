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

import csv

from django.core.management.base import BaseCommand

from core.models import TeachingModel
from core.adminsettings.importclass import EDTTextSyncCourses


class Command(BaseCommand):
    help = "Sync courses from an EDT export file."

    def add_arguments(self, parser):
        parser.add_argument(
            "export", help="Export file from EDT must be the list of given courses."
        )
        parser.add_argument("teaching", help="The teaching where the sync has to be done.")
        parser.add_argument(
            "group_relation", help="A csv file with two columns, the matricule and the group number"
        )

    def handle(self, *args, **options):
        teaching = TeachingModel.objects.get(name=options["teaching"])
        edt_sync = EDTTextSyncCourses(teaching, options["group_relation"])

        with open(options["export"], "r", encoding="UTF-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            edt_sync.sync(reader)
