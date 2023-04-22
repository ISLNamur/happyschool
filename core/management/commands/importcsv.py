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
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from core.models import TeachingModel
from core.adminsettings.importclass import ImportStudentCSV, ImportResponsibleCSV


class Command(BaseCommand):
    help = "Import a csv file for student or teachers."

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--student",
            help="Path to students csv file. Expected header columns: 'Nom Elève', 'Prénom Elève',"
            " 'Matric Info', 'Année', 'Classe'",
        )

        parser.add_argument(
            "-t",
            "--teacher",
            help="Path to teacher csv file. Expected header columns: 'Nom Enseignant',"
            " 'Prénom Enseignant', 'Matricule Ministère', 'Classe'",
        )

        parser.add_argument(
            "implementation",
            help="Implementation of the related people i.e. teaching field of the person.",
        )

    def handle(self, *args, **options):
        if options["student"]:
            with open(options["student"], newline="", encoding="utf-8-sig") as student_csv:
                try:
                    teaching = TeachingModel.objects.get(name=options["implementation"])
                except ObjectDoesNotExist:
                    teaching = TeachingModel(
                        name=options["implementation"],
                        display_name=options["implementation"].title(),
                    )
                column_map = {
                    "Matric Info": "matricule",
                    "Nom Elève": "last_name",
                    "Prénom Elève": "first_name",
                    "Année": "year",
                    "Classe": "classe_letter",
                    "Email": "email",
                }
                import_student_csv = ImportStudentCSV(teaching, column_map)
                import_student_csv.sync(student_csv, has_header=True)

        if options["teacher"]:
            with open(options["teacher"], newline="", encoding="utf-8-sig") as teacher_csv:
                try:
                    teaching = TeachingModel.objects.get(name=options["implementation"])
                except ObjectDoesNotExist:
                    teaching = TeachingModel(
                        name=options["implementation"],
                        display_name=options["implementation"].title(),
                    )
                column_map = {
                    "Matricule Ministère": "matricule",
                    "Nom Enseignant": "last_name",
                    "Prénom Enseignant": "first_name",
                    "Classe": "classe",
                    "Email": "email",
                }
                import_teacher_csv = ImportResponsibleCSV(teaching, column_map, is_teacher=True)
                import_teacher_csv.sync(teacher_csv, has_header=True)
        return
