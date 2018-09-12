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
            student_synced = set()
            processed = 0
            with open(options['student'], newline='') as student_csv:
                reader = csv.reader(student_csv, )
                header = next(reader, None)
                column_map = {j: i for i, j in enumerate(header)}
                for row in reader:
                    matricule = row[column_map['Matric Info']]
                    last_name = row[column_map['Nom Elève']]
                    first_name = row[column_map['Prénom Elève']]
                    year = row[column_map['Année']][0]
                    if not year.isdigit() and len(year) > 1:
                        year = row[column_map['Année']][1]

                    classe_letter = row[column_map['Classe']].lower()

                    # Ignore students with empty values.
                    if len(year) == 0 or len(classe_letter) == 0:
                        print("Ignore %s %s, year or classe letter wrongly formatted!" % (last_name, first_name))
                        continue

                    try:
                        student = StudentModel.objects.get(matricule=int(matricule))
                        student.inactive_from = None
                    except ObjectDoesNotExist:
                        student = StudentModel(matricule=int(matricule))

                    # Check if student's teaching already exists.
                    try:
                        teaching = TeachingModel.objects.get(name=options["implementation"])
                    except ObjectDoesNotExist:
                        teaching = TeachingModel(name=options["implementation"],
                                                 display_name=options["implementation"].title())
                        teaching.save()

                    student.teaching = teaching

                    # Check if student's classe already exists.
                    try:
                        classe = ClasseModel.objects.get(year=int(year),
                                                         letter=classe_letter,
                                                         teaching=teaching)
                    except ObjectDoesNotExist:
                        classe = ClasseModel(year=int(year),
                                             letter=classe_letter,
                                             teaching=teaching)
                        classe.save()

                    student.classe = classe
                    student.first_name = first_name
                    student.last_name = last_name
                    student.save()

                    student_synced.add(student.matricule)

                    # Print progress.
                    processed += 1
                    if processed % 50 == 0:
                        print(processed)

            # Remove removed students.
            all_students = StudentModel.objects.filter(teaching__name=options["implementation"])
            for s in all_students:
                if s.matricule not in student_synced:
                    s.inactive_from = timezone.make_aware(timezone.datetime.now())
                    s.classe = None
                    s.save()

        if options['teacher']:
            teacher_synced = set()
            processed = 0
            with open(options['teacher'], newline='') as teacher_csv:
                reader = csv.reader(teacher_csv, )
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

