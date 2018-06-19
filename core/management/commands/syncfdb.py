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
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone

from core.models import *
from core.utilities import get_scholar_year


class Command(BaseCommand):
    help = 'Sync django database with a ProEco database.'

    def handle(self, *args, **options):
        from libreschoolfdb import reader

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
            proeco_students = reader.get_students(year=current_year, fdb_server=proeco["server"], teaching=proeco["teaching_type"])
            print("%s students found" % len(proeco_students))
            processed = 0
            for matricule, s in proeco_students.items():
                try:
                    student = StudentModel.objects.get(matricule=matricule)
                except ObjectDoesNotExist:
                    student = StudentModel(matricule=matricule)

                student.teaching = teaching_model

                # Check if student's classe already exists.
                try:
                    classe = ClasseModel.objects.get(year=s['classe_year'],
                                                     letter=s['classe_letter'].lower(), teaching=teaching_model)
                except ObjectDoesNotExist:
                    classe = ClasseModel(year=s['classe_year'], letter=s['classe_letter'].lower(),
                                         teaching=teaching_model)
                    classe.save()

                student.classe = classe
                student.first_name = s['firstname']
                student.last_name = s['surname']
                student.save()

                # Additional info.
                try:
                    info = student.additionalstudentinfo
                except ObjectDoesNotExist:
                    info = AdditionalStudentInfo(student=student)

                info.gender = s['gender']
                info.scholar_year = s['year']
                # info.previous_classe = s['previous_classe'] # TODO Implement previous classe.
                info.orientation = s['orientation']

                info.birth_date = date(year=int(str(s['birth_date'])[:4]),
                                       month=int(str(s['birth_date'])[4:6]),
                                       day=int(str(s['birth_date'])[6:]))
                info.street = s['address']
                info.postal_code = s['postal_code']
                info.locality = s['city']

                info.student_phone = s['student_phone']
                info.student_mobile = s['student_phone']
                info.student_email = s['student_email']

                info.resp_last_name = s['resp_surname']
                info.resp_first_name = s['resp_firstname']
                info.resp_phone = s['phone']
                info.resp_mobile = s['gsm']
                info.resp_email = s['email']

                info.father_last_name = s['father_surname']
                info.father_first_name = s['father_firstname']
                info.father_job = s['father_job']
                info.father_phone = s['father_phone']
                info.father_mobile = s['father_gsm']
                info.father_email = s['father_email']

                info.mother_last_name = s['mother_surname']
                info.mother_first_name = s['mother_firstname']
                info.mother_job = s['mother_job']
                info.mother_phone = s['mother_phone']
                info.mother_mobile = s['mother_gsm']
                info.mother_email = s['mother_email']

                info.doctor = s['medecin']
                info.doctor_phone = s['medecin_phone']
                info.mutual = s['mutuelle']
                info.mutual_number = s['mutuelle_num']
                info.medical_information = s['medical_info']

                info.save()

                student_synced.add(student.matricule)
                processed += 1
                if processed % 50 == 0:
                    print(processed)

            # Set removed students as inactive.
            all_students = StudentModel.objects.all()
            for s in all_students:
                if s.matricule not in student_synced:
                    s.inactive_from = timezone.make_aware(timezone.datetime.now())
                    s.classe = None
                    s.save()

            # Sync teachers.
            teachers = reader.get_teachers(year=current_year,
                                           fdb_server=proeco["server"],
                                           teaching=proeco["teaching_type"])
            print("%s teachers found" % len(teachers))
            processed = 0
            teachers_synced = set()
            for matricule, t in teachers.items():
                resp = self.update_responsible(responsible_type="teacher",
                                        matricule=matricule,
                                        data=t,
                                        teaching_model=teaching_model)
                teachers_synced.add(resp.matricule)
                processed += 1
                if processed % 25 == 0:
                    print(processed)

            # Set inactive teachers.
            all_teachers = ResponsibleModel.objects.filter(is_teacher=True, teaching__in=[teaching_model])
            for t in all_teachers:
                if t.matricule not in teachers_synced:
                    if not t.inactive_from:
                        print("Set %s as inactive" % t.fullname)
                        t.inactive_from = timezone.make_aware(timezone.datetime.now())
                    t.classe.clear()
                    t.tenure.clear()
                    t.teaching.clear()
                    t.save()

            # Sync educators.
            educators = reader.get_educators(fdb_server=proeco["server"])
            print("%s educators found" % len(educators))
            processed = 0
            educators_synced = set()
            for matricule, e in educators.items():
                resp = self.update_responsible(responsible_type="educator",
                                               matricule=matricule,
                                               data=e,
                                               teaching_model=teaching_model)
                educators_synced.add(resp.matricule)
                processed += 1
                if processed % 25 == 0:
                    print(processed)

            # Set inactive educators.
            all_educators = ResponsibleModel.objects.filter(is_educator=True, teaching__in=[teaching_model])
            for e in all_educators:
                if e.matricule not in educators_synced:
                    if not e.inactive_from:
                        print("Set %s as inactive" % e.fullname)
                        e.inactive_from = timezone.make_aware(timezone.datetime.now())
                    e.classe.clear()
                    e.tenure.clear()
                    e.teaching.clear()
                    e.save()

    def update_responsible(self, responsible_type, matricule, data, teaching_model):
        # Check if the responsible already exists.
        try:
            resp = ResponsibleModel.objects.get(matricule=matricule)
        except ObjectDoesNotExist:
            resp = ResponsibleModel(matricule=matricule)

        if responsible_type == 'teacher':
            resp.is_teacher = True

        if responsible_type == 'educator':
            resp.is_educator = True

        resp.save()
        resp.teaching.add(teaching_model)

        # Check if responsible's classes already exists.
        if responsible_type == 'teacher' and "classes" in data:
            for c in data['classes']:
                try:
                    classe = ClasseModel.objects.get(year=int(c[0]), letter=c[1].lower(), teaching=teaching_model)
                except ObjectDoesNotExist:
                    classe = ClasseModel(year=int(c[0]), letter=c[1].lower(), teaching=teaching_model)
                    classe.save()
                resp.classe.add(classe)

        # Check if responsible's tenures already exists.
        if responsible_type == 'teacher' and data['tenure']:
            try:
                tenure = ClasseModel.objects.get(year=int(data['tenure'][0]), letter=data['tenure'][1].lower(),
                                                 teaching=teaching_model)
            except ObjectDoesNotExist:
                tenure = ClasseModel(year=int(data['tenure'][0]), letter=data['tenure'][1].lower(),
                                     teaching=teaching_model)
                tenure.save()
            resp.tenure.add(tenure)
            resp.classe.add(tenure)

        if "email" in data:
            resp.email = data['email']

        resp.first_name = data['firstname']
        resp.last_name = data['surname']
        resp.save()
        return resp
