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

from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from core.utilities import get_scholar_year
from core.models import TeachingModel, StudentModel
from student_absence.models import StudentAbsenceModel, JustificationModel


class Command(BaseCommand):
    help = 'Import a ProEco database into HappySchool.'

    def handle(self, *args, **options):
        from libreschoolfdb import reader
        from libreschoolfdb.absences import Absence

        proecos = settings.SYNC_FDB_SERVER
        current_year = get_scholar_year()

        student_synced = set()
        for proeco in proecos:
            try:
                teaching_model = TeachingModel.objects.get(name=proeco["teaching_name"])
            except ObjectDoesNotExist:
                print("teaching__name: %s, not found" % proeco["teaching_name"])
                continue

            # ProEco student list.
            proeco_students = reader.get_students(year=current_year, fdb_server=proeco["server"],
                                                  teaching=proeco["teaching_type"], med_info=False, parents_info=False)
            print("%s students found" % len(proeco_students))
            processed = 0
            for matricule, s in proeco_students.items():
                processed += 1
                if processed % 50 == 1:
                    print(processed - 1)
                try:
                    student = StudentModel.objects.get(matricule=matricule)
                except ObjectDoesNotExist:
                    # No student found, ignoring.
                    continue

                # Import absences.
                absences = s['absences']
                absences_processed = set()
                for a in absences:
                    try:
                        absence = StudentAbsenceModel.objects.get(student=student, date_absence=a.date)
                        absence.morning = a.morning
                        absence.afternoon = a.afternoon
                        absence.save()
                    except:
                        absence = StudentAbsenceModel.objects.create(student=student, date_absence=a.date,
                                                                     morning=a.morning, afternoon=a.afternoon)
                    absences_processed.add(absence.pk)

                # Remove deleted absences.
                StudentAbsenceModel.objects.filter(student=student).exclude(pk__in=absences_processed).delete()

                # Import justifications.
                justifications = s['absences_justifications']
                # Clean first.
                JustificationModel.objects.filter(student=student).delete()
                for j in justifications:
                    JustificationModel.objects.create(student=student,
                                                      date_just_start=j['start'][0], date_just_end=j['end'][0],
                                                      half_day_start=j['start'][1], half_day_end=j['end'][1],
                                                      short_name=j['code'], half_days=j['half_days'])
