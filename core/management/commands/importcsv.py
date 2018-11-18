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

from core.models import StudentModel, TeachingModel, ClasseModel, ResponsibleModel
from core.adminsettings.importclass import ImportStudentCSV


class Command(BaseCommand):
    help = 'Import a csv file for student or teachers.'

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            '--student',
            help="Path to students csv file. Expected header columns: 'Nom Elève', 'Prénom Elève', 'Matric Info', 'Année', 'Classe'"
        )

        parser.add_argument(
            "-t",
            '--teacher',
            help="Path to teacher csv file. Expected header columns: 'Nom Enseignant', 'Prénom Enseignant', 'Matricule Ministère'"
        )

        parser.add_argument(
            "implementation",
            help="Implementation of the related people i.e. teaching field of the person."
        )

    def handle(self, *args, **options):
        if options['student']:
            with open(options['student'], newline='', encoding="utf-8-sig") as student_csv:
                try:
                    teaching = TeachingModel.objects.get(name=options["implementation"])
                except ObjectDoesNotExist:
                    teaching = TeachingModel(name=options["implementation"],
                                             display_name=options["implementation"].title())
                column_map = {'Matric Info': 'matricule', 'Nom Elève': 'last_name',
                              'Prénom Elève': 'first_name', 'Année': 'year',
                              'Classe': 'classe_letter'}
                import_student_csv = ImportStudentCSV(teaching, column_map)
                import_student_csv.sync(student_csv, has_header=True)

        if options['teacher']:
            teacher_synced = set()
            processed = 0
            with open(options['teacher'], newline='') as teacher_csv:
                dialect = csv.Sniffer().sniff(teacher_csv.read(1024))
                teacher_csv.seek(0)
                reader = csv.reader(teacher_csv, dialect)
                header = next(reader, None)
                column_map = {j: i for i, j in enumerate(header)}
                for row in reader:
                    matricule = row[column_map['Matricule Ministère']]
                    last_name = row[column_map['Nom Enseignant']]
                    first_name = row[column_map['Prénom Enseignant']]

                    try:
                        teacher = ResponsibleModel.objects.get(matricule=int(matricule))
                        teacher.inactive_from = None
                    except ObjectDoesNotExist:
                        teacher = ResponsibleModel(matricule=int(matricule), is_teacher=True)

                    teacher.first_name = first_name
                    teacher.last_name = last_name
                    teacher.save()

                    # Check if teacher's teaching already exists.
                    try:
                        teaching = TeachingModel.objects.get(name=options["implementation"])
                    except ObjectDoesNotExist:
                        teaching = TeachingModel(name=options["implementation"],
                                                 display_name=options["implementation"].title())
                        teaching.save()

                    teacher.teaching.add(teaching)



                    teacher_synced.add(teacher.matricule)

                    # Print progress.
                    processed += 1
                    if processed % 25 == 0:
                        print(processed)

            # Remove removed teachers.
            all_teachers = ResponsibleModel.objects.filter(teaching__name=options["implementation"],
                                                           is_teacher=True)
            for t in all_teachers:
                if t.matricule not in teacher_synced:
                    t.inactive_from = timezone.make_aware(timezone.datetime.now())
                    t.save()
        return

