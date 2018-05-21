from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from core.models import *
from core.ldap import get_ldap_connection, get_django_dict_from_ldap


class Command(BaseCommand):
    help = 'Sync django database from a LDAP server.'

    def handle(self, *args, **options):
        connection = get_ldap_connection()
        base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
        # Get all students.
        print("Retrieving students")
        student_synced = set()
        connection.search(base_dn, "(objectClass=eleve)", attributes='*')
        print("%s students found" % len(connection.response))
        processed = 0
        # Add/update students.
        for s in connection.response:
            student_dict = get_django_dict_from_ldap(s)
            # Check if the student already exists.
            try:
                student = StudentModel.objects.get(matricule=int(student_dict['matricule']))
            except ObjectDoesNotExist:
                student = StudentModel(matricule=int(student_dict['matricule']))

            # Check if student's teaching already exists.
            try:
                teaching = TeachingModel.objects.get(name=student_dict['teaching'][0])
            except ObjectDoesNotExist:
                teaching = TeachingModel(name=student_dict['teaching'][0], display_name=student_dict['teaching'][0].title())
                teaching.save()

            student.teaching = teaching

            # Check if student's classe already exists.
            try:
                classe = ClasseModel.objects.get(year=student_dict['year'], letter=student_dict['classe_letter'].lower(), teaching=teaching)
            except ObjectDoesNotExist:
                classe = ClasseModel(year=student_dict['year'], letter=student_dict['classe_letter'].lower(), teaching=teaching)
                classe.save()

            student.classe = classe
            student.first_name = student_dict['first_name']
            student.last_name = student_dict['last_name']
            student.save()

            # Additional info.
            try:
                info = student.additionalstudentinfo
            except ObjectDoesNotExist:
                info = AdditionalStudentInfo(student=student)

            info.gender = student_dict['gender']
            info.scholar_year = student_dict['scholar_year']
            info.previous_classe = student_dict['previous_classe']
            info.orientation = student_dict['orientation']

            info.birth_date = student_dict['birth_date']
            info.street = student_dict['street']
            info.postal_code = student_dict['postal_code']
            info.locality = student_dict['locality']

            info.student_phone = student_dict['student_phone']
            info.student_mobile = student_dict['student_phone']
            info.student_email = student_dict['student_email']

            info.resp_last_name = student_dict['resp_last_name']
            info.resp_first_name = student_dict['resp_first_name']
            info.resp_phone = student_dict['resp_phone']
            info.resp_mobile = student_dict['resp_mobile']
            info.resp_email = student_dict['resp_email']

            info.father_last_name = student_dict['father_last_name']
            info.father_first_name = student_dict['father_first_name']
            info.father_job = student_dict['father_job']
            info.father_phone = student_dict['father_phone']
            info.father_mobile = student_dict['father_mobile']
            info.father_email = student_dict['father_email']

            info.mother_last_name = student_dict['mother_last_name']
            info.mother_first_name = student_dict['mother_first_name']
            info.mother_job = student_dict['mother_job']
            info.mother_phone = student_dict['mother_phone']
            info.mother_mobile = student_dict['mother_mobile']
            info.mother_email = student_dict['mother_email']

            info.doctor = student_dict['doctor']
            info.doctor_phone = student_dict['doctor_phone']
            info.mutual = student_dict['mutual']
            info.mutual_number = student_dict['mutual_number']
            info.medical_information = student_dict['medical_information']

            info.username = student_dict['username']
            info.password = student_dict['password']
            info.save()

            student_synced.add(student.matricule)
            processed += 1
            if processed % 50 == 0:
                print(processed)

        # Remove removed students.
        all_students = StudentModel.objects.all()
        for s in all_students:
            if s.matricule not in student_synced:
                s.delete()

        # Get all responsibles.
        print("Retrieving responsibles")
        connection.search(base_dn, "(objectClass=responsible)", attributes='*')
        print("%s responsibles found" % len(connection.response))
        processed = 0
        resp_synced = set()
        for r in connection.response:
            resp_dict = get_django_dict_from_ldap(r)
            # Check if the responsible already exists.
            try:
                resp = ResponsibleModel.objects.get(matricule=int(resp_dict['matricule']))
            except ObjectDoesNotExist:
                try:
                    user = User.objects.get(username=resp_dict['username'])
                except ObjectDoesNotExist:
                    user = User.objects.create_user(resp_dict['username'])
                resp = ResponsibleModel(matricule=int(resp_dict['matricule']), user=user)

            if 'professeur' in r['attributes']['objectClass']:
                resp.is_teacher = True

            if 'educateur' in r['attributes']['objectClass']:
                resp.is_educator = True

            resp.save()
            # Check if responsible's teaching already exists.
            for t in resp_dict['teaching']:
                try:
                    teaching = TeachingModel.objects.get(name=t)
                except ObjectDoesNotExist:
                    teaching = TeachingModel(name=t, display_name=t.title())
                    teaching.save()
                resp.teaching.add(teaching)

            # Check if responsible's classes already exists.
            if 'classe' in resp_dict:
                for c in resp_dict['classe']:
                    try:
                        classe = ClasseModel.objects.get(year=int(c[0]), letter=c[1].lower(), teaching=teaching)
                    except ObjectDoesNotExist:
                        classe = ClasseModel(year=int(c[0]), letter=c[1].lower(), teaching=teaching)
                        classe.save()
                    resp.classe.add(classe)

            # Check if responsible's tenures already exists.
            if 'tenure' in resp_dict:
                for t in resp_dict['tenure']:
                    try:
                        tenure = ClasseModel.objects.get(year=int(t[0]), letter=t[1].lower(), teaching=teaching)
                    except ObjectDoesNotExist:
                        tenure = ClasseModel(year=int(t[0]), letter=t[1].lower(), teaching=teaching)
                        tenure.save()
                    resp.tenure.add(tenure)
                    resp.classe.add(tenure)

            if 'resp_email' in resp_dict:
                resp.email = resp_dict['resp_email']

            if 'gen_email' in resp_dict:
                resp.email_alias = resp_dict['gen_email']

            resp.first_name = resp_dict['first_name']
            resp.last_name = resp_dict['last_name']
            resp.save()
            resp_synced.add(resp.matricule)
            processed += 1
            if processed % 25 == 0:
                print(processed)

        # Remove removed responsibles.
        all_resp = ResponsibleModel.objects.all()
        for r in all_resp:
            if r.matricule not in resp_synced:
                r.delete()