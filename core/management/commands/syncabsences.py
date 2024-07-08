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

import sys
from datetime import date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q

from core.utilities import get_scholar_year
from core.models import TeachingModel, StudentModel
from student_absence_teacher.models import (
    JustificationModel,
    StudentAbsenceEducModel,
    PeriodEducModel,
    JustMotiveModel,
)

class Command(BaseCommand):
    help = "Import a ProEco database into HappySchool."

    def handle(self, *args, **options):
        from libreschoolfdb.absences import get_all_absences, get_all_justifications

        proecos = settings.SYNC_FDB_SERVER
        current_year = get_scholar_year()

        for proeco in proecos:
            absences = get_all_absences(23, fdb_server=proeco["server"])

            for matricule, absences_stud in absences.items():
                try:
                    student = StudentModel.objects.get(matricule=matricule)
                except ObjectDoesNotExist:
                    # No student found, ignoring.
                    continue

                # Import absences.
                absences_processed = set()
                for a in absences_stud:
                    period = PeriodEducModel.objects.all().order_by("start")[a.period]
                    try:
                        absence = StudentAbsenceEducModel.objects.get(
                            student=student, date_absence=a.date, period=period
                        )
                        absence.status = a.status
                        absence.save()
                    except ObjectDoesNotExist:
                        absence = StudentAbsenceEducModel.objects.create(
                            student=student,
                            date_absence=a.date,
                            period=period,
                            status=a.status,
                        )
                    except MultipleObjectsReturned:
                        print(student, a.date, period)
                        multiple = StudentAbsenceEducModel.objects.filter(
                            student=student, date_absence=a.date, period=period
                        )
                        print(multiple)
                        continue
                    absences_processed.add(absence.pk)

                # Remove deleted absences.
                StudentAbsenceEducModel.objects.filter(student=student).exclude(
                    pk__in=absences_processed
                ).delete()


            justifications = get_all_justifications(23, fdb_server=proeco["server"])
            for matricule, just in justifications.items():
                try:
                    student = StudentModel.objects.get(matricule=matricule)
                except ObjectDoesNotExist:
                    # No student found, ignoring.
                    continue

                # Clean first.
                JustificationModel.objects.filter(student=student).delete()

                periods = list(enumerate(PeriodEducModel.objects.all().order_by("start")))

                for j in just:
                    motive = JustMotiveModel.objects.get(short_name=j["motive"])
                    just = JustificationModel.objects.create(
                        student=student,
                        date_just_start=j["start_date"],
                        date_just_end=j["end_date"],
                        half_day_start=j["start_period"],
                        half_day_end=j["end_period"],
                        motive=motive,
                        comment=j["comment"],
                    )

                    # ProEco periods are listed by indices. Find the associated period model.
                    start_periods = [
                        p
                        for i, p in periods
                        if i >= just.half_day_start
                    ]
                    end_periods = [
                        p
                        for i, p in periods
                        if i <= just.half_day_end
                    ]

                    related_absences = StudentAbsenceEducModel.objects.filter(status="A", student=student).filter(
                        Q(date_absence__gt=just.date_just_start, date_absence__lt=just.date_just_end)
                        | Q(date_absence=just.date_just_start, period__in=start_periods)
                        | Q(date_absence=just.date_just_end, period__in=end_periods)
                    )

                    just.absences.set(related_absences)
                    
