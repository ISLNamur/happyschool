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
from typing import Union, TextIO
from datetime import date

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User, Group

from core.models import StudentModel, TeachingModel, ClasseModel, AdditionalStudentInfo,\
    ResponsibleModel, CourseModel, GivenCourseModel
from core.ldap import get_ldap_connection, get_django_dict_from_ldap
from core.utilities import get_scholar_year


class ImportBase:
    """Base class to import students and responsible"""

    def __init__(self, teaching: TeachingModel) -> None:
        self.teaching = teaching

    def _sync(self, iterable) -> None:
        pass

    """Get value from an entry."""
    def get_value(self, entry: object, column: str) -> Union[int, str, date, None]:
        try :
            return self.format_value(entry[column], column)
        except KeyError:
            return None

    """Handle different entry format."""
    def format_value(self, value: Union[int, str], column: str) -> Union[int, date, str, None]:
        return value

    """Print progress"""
    def print_log(self, log: str) -> None:
        print(log)


class ImportResponsible(ImportBase):
    """Base class for importing responsibles."""
    search_login_directory = False
    ldap_unique_attr = "matricule"
    has_inactivity = False
    ldap_connection = None
    username_attribute = "username"
    base_dn = None

    def __init__(self, teaching: TeachingModel) -> None:
        super().__init__(teaching)

    def get_responsible(self, entry):
        matricule = int(self.get_value(entry, "matricule"))
        if not matricule:
            return None
        try:
            return ResponsibleModel.objects.get(matricule=matricule)
        except ObjectDoesNotExist:
            return ResponsibleModel(matricule=matricule)

    def _sync(self, iterable) -> None:
        if not self.teaching:
            self.print_log("teaching is missing, aborting.")
            return
        processed = 0
        resp_synced = set()
        if self.search_login_directory:
            self.ldap_connection = get_ldap_connection()
            self.base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
        self.print_log("Importing responsibles…(%s)" % self.teaching.display_name)
        for entry in iterable:
            # First check mandatory field.
            first_name = self.get_value(entry, "first_name")
            if not first_name:
                self.print_log("No first name found, skipping responsible.")
                continue
            last_name = self.get_value(entry, "last_name")
            if not last_name:
                self.print_log("No last name found, skipping responsible.")
                continue
            resp = self.get_responsible(entry)
            if not resp:
                self.print_log("No unique identifier found, skipping responsible.")
                continue
            username = self.get_value(entry, self.username_attribute)
            if self.search_login_directory:
                matricule = self.get_value(entry, "matricule")
                self.ldap_connection.search(self.base_dn, "(%s=%i)" % (self.ldap_unique_attr, matricule),
                                            attributes='*')
                for r in self.ldap_connection.response:
                    ldap_info = get_django_dict_from_ldap(r)
                    username = ldap_info['username']
            if username and len(username.strip(" ")) > 0:
                try:
                    user = User.objects.get(username=username)
                except ObjectDoesNotExist:
                    user = User.objects.create_user(username)
                user.last_name = last_name
                user.first_name = first_name

                if "email" in self.username_attribute:
                    user.email = user.username
                user.save()
                resp.user = user

            resp.first_name = first_name
            resp.last_name = last_name
            resp.inactive_from = None
            resp.save()

            resp.teaching.add(self.teaching)

            if self.has_inactivity:
                inactive_from = self.get_value(entry, "inactive_from")
                if inactive_from:
                    resp.inactive_from = timezone.make_aware(
                        timezone.datetime.combine(inactive_from, timezone.datetime.min.time()))
                else:
                    resp.inactive_from = None

            educ_group = Group.objects.get(name="educateur")
            is_educator = self.get_value(entry, "is_educator")
            if is_educator:
                resp.is_educator = True
                if resp.user:
                    educ_group.user_set.add(resp.user)
            teach_group = Group.objects.get(name="professeur")
            is_teacher = self.get_value(entry, "is_teacher")
            if is_teacher:
                resp.is_teacher = True
                if resp.user:
                    teach_group.user_set.add(resp.user)

            # Update classes and course only for teachers
            if is_teacher:
                # Check if responsible's classes already exists.
                if resp.matricule not in resp_synced:
                    resp.classe.remove(*resp.classe.filter(teaching=self.teaching))
                    resp.courses.remove(*resp.courses.filter(course__teaching=self.teaching))
                classe = self.get_value(entry, "classe")
                if classe and type(classe) != list:
                    classe = [classe]
                if classe:
                    for c in classe:
                        if len(c) < 2:
                            continue
                        try:
                            classe_model = ClasseModel.objects.get(year=int(c[0]), letter=c[1:].lower(),
                                                                teaching=self.teaching)
                        except ObjectDoesNotExist:
                            classe_model = ClasseModel(year=int(c[0]), letter=c[1:].lower(),
                                                    teaching=self.teaching)
                            classe_model.save()
                        resp.classe.add(classe_model)

                courses = self.get_value(entry, "courses")
                if courses and type(courses) != list:
                    courses = [courses]
                if courses:
                    for c in courses:
                        if not c["classes"]:
                            continue
                        try:
                            course_model = CourseModel.objects.get(id=c["id"])
                        except ObjectDoesNotExist:
                            course_model = CourseModel(id=c["id"], name=c["name"], teaching=self.teaching)
                            course_model.save()
                        try:
                            given_course = GivenCourseModel.objects.get(course=course_model, group=c["group"])
                        except ObjectDoesNotExist:
                            given_course = GivenCourseModel(course=course_model, group=c["group"])
                            given_course.save()
                        resp.courses.add(given_course)

                # Check if responsible's tenures already exists.
                if resp.matricule not in resp_synced:
                    resp.tenure.clear()
                tenure = self.get_value(entry, "tenure")
                if tenure:
                    if type(tenure) == str:
                        tenure = [tenure]
                    for t in tenure:
                        try:
                            tenure_model = ClasseModel.objects.get(year=int(t[0]), letter=t[1:].lower(),
                                                                teaching=self.teaching)
                        except ObjectDoesNotExist:
                            tenure_model = ClasseModel(year=int(t[0]), letter=t[1:].lower(),
                                                    teaching=self.teaching)
                            tenure_model.save()
                        resp.tenure.add(tenure_model)
                        resp.classe.add(tenure_model)

            email = self.get_value(entry, "email")
            email_school = self.get_value(entry, "email_school")
            if email:
                resp.email = email
            if email_school:
                resp.email_school = email_school

            birth_date = self.get_value(entry, "birth_date")
            if birth_date:
                resp.birth_date = birth_date

            resp.save()
            if not resp.matricule in resp_synced:
                processed += 1
                if processed % 50 == 0:
                    self.print_log(processed)
            if is_teacher:
                resp_synced.add(resp.matricule)

        # Set inactives teachers.
        if len(resp_synced) != 0:
            self.print_log("Set inactive teachers…")
            all_resp = ResponsibleModel.objects.filter(teaching=self.teaching, is_teacher=True)
            for r in all_resp:
                if r.matricule not in resp_synced:
                    if not self.has_inactivity:
                        r.inactive_from = timezone.make_aware(timezone.datetime.now())
                        r.classe.clear()
                        r.tenure.clear()
                        r.courses.clear()
                        r.save()
                    else:
                        r.delete()

        self.print_log("Import done.")


class ImportResponsibleLDAP(ImportResponsible):
    search_login_directory = False
    has_inactivity = True

    def __init__(self, teaching: TeachingModel) -> None:
        super().__init__(teaching=teaching)
        self.connection = get_ldap_connection()
        self.base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn

    def sync(self):
        self.connection.search(self.base_dn,
                               "(&(objectClass=responsible)(enseignement=%s))" % self.teaching.name,
                               attributes='*')
        ldap_entries = map(lambda entry: get_django_dict_from_ldap(entry), self.connection.response)
        super()._sync(ldap_entries)

    def get_responsible(self, entry):
        matricule = int(self.get_value(entry, "matricule"))
        if not matricule:
            return None

        try:
            return ResponsibleModel.objects.get(matricule=matricule)
        except ObjectDoesNotExist:
            # It may happen that responsible has a temporary matricule, search by email instead.
            try:
                email = self.get_value(entry, "email")
                if not email:
                    raise
                resp = ResponsibleModel.objects.get(email=email)
                # Set definitive matricule.
                resp.matricule = matricule
                return resp
            except ObjectDoesNotExist:
                return ResponsibleModel(matricule=matricule)


class ImportResponsibleCSV(ImportResponsible):
    def __init__(self, teaching: TeachingModel, column_map: dict = None,
                 column_index: dict = None, is_teacher: bool = False,
                 is_educator: bool = False) -> None:

        super().__init__(teaching=teaching)
        self.is_teacher = is_teacher
        self.is_educator = is_educator
        self.column_map = column_map
        if not column_index:
            self.column_to_index = {j: i for i, j in
                                    enumerate(["matricule", "last_name", "first_name",
                                               "classe", "tenure"])}
        else:
            self.column_to_index = column_index

    def sync(self, text: TextIO, ignore_first_line: bool=False,
             has_header: bool=False) -> None:
        # First detect dialect.
        dialect = csv.Sniffer().sniff(text.readline())
        # Return to start.
        text.seek(0)

        reader = csv.reader(text, dialect)
        if ignore_first_line:
            next(reader, None)
        # Map column to row index with first line.
        if has_header:
            header = next(reader, None)
            if self.column_map:
                self.column_to_index = {self.column_map[j]: i for i, j in
                                        enumerate(header)}
            else:
                self.column_to_index = {j: i for i, j in
                                        enumerate(header)}

        super()._sync(reader)

    def get_value(self, entry: list, column: str) -> Union[int, str, date, None]:
        if column == "is_teacher":
            return self.is_teacher
        if column == "is_educator":
            return self.is_educator
        try:
            return self.format_value(entry[self.column_to_index[column]], column)
        except KeyError:
            return None


class ImportResponsibleFDB(ImportResponsible):
    column_map = {
        "last_name": "surname", "first_name": "firstname", "classe": "classes",
    }
    is_teacher = False
    is_educator = False

    def __init__(self, teaching: TeachingModel, fdb_server, search_login_directory: bool,
                 teaching_type: str, ldap_unique_attr="matricule", classe_format="%C",
                 username_attribute=None) -> None:
        super().__init__(teaching)
        self.server = fdb_server
        self.teaching_type = teaching_type
        self.search_login_directory = search_login_directory
        self.ldap_unique_attr = ldap_unique_attr
        self.classe_format = classe_format
        if username_attribute:
            self.username_attribute = username_attribute

    def sync(self) -> None:
        from libreschoolfdb.reader import get_teachers, get_educators
        year = get_scholar_year()
        self.print_log("Collecting teachers from ProEco database…")
        teachers = get_teachers(year, self.server, self.teaching_type,
                                classe_format=self.classe_format)
        self.is_teacher = True
        self.is_educator = False
        self._sync(teachers.items())

        self.print_log("Collecting educators from ProEco database…")
        educators = get_educators(self.server)
        self.is_teacher = False
        self.is_educator = True
        self._sync(educators.items())

    def get_value(self, entry: dict, column: str) -> Union[int, str, date, None]:
        if "proeco" in settings.INSTALLED_APPS:
            from proeco.models import OverwriteDataModel
            try:
                overwrite = OverwriteDataModel.objects.get(
                    people="responsible",
                    uid=entry[0],
                    field=column
                )
                return overwrite.value
            except ObjectDoesNotExist:
                pass

        if column == "matricule":
            return entry[0]
        if column == "is_teacher":
            return self.is_teacher
        if column == "is_educator":
            return self.is_educator
        elif column == "username" or column == "password":
            return None
        elif column in self.column_map:
            if self.column_map[column] in entry[1]:
                return entry[1][self.column_map[column]]
            else:
                return None
        else:
            if column in entry[1]:
                return self.format_value(entry[1][column], column)
            return None

    def get_responsible(self, entry):
        matricule = int(self.get_value(entry, "matricule"))
        if not matricule:
            return None

        try:
            return ResponsibleModel.objects.get(matricule=matricule)
        except ObjectDoesNotExist:
            # It may happen that responsible has a temporary matricule, search by email instead.
            try:
                email = self.get_value(entry, "email")
                if not email:
                    raise
                resp = ResponsibleModel.objects.get(email=email)
                # Set definitive matricule.
                resp.matricule = matricule
                return resp
            except ObjectDoesNotExist:
                return ResponsibleModel(matricule=matricule)


class ImportStudent(ImportBase):
    """Base class for importing students."""

    additional_columns = [
        "gender", "scholar_year", "previous_class",
        "orientation", "street", "postal_code",
        "locality", "student_phone", "student_mobile",
        "student_email", "resp_last_name", "resp_first_name",
        "resp_phone", "resp_mobile", "resp_email",
        "father_last_name", "father_first_name",
        "father_job", "father_phone", "father_mobile",
        "father_email",
        "mother_last_name", "mother_first_name",
        "mother_job","mother_phone", "mother_mobile",
        "mother_email",
        "doctor", "doctor_phone", "mutual",
        "medical_information",
        "birth_date", "username", "password",
    ]
    ldap_connection = None
    base_dn = None

    def __init__(self, teaching: TeachingModel, search_login_directory: bool = False) -> None:
        super().__init__(teaching)
        self.search_login_directory = search_login_directory

    def format_value(self, value: Union[int, str], column: str) -> Union[int, str, date, None]:
        if type(value) == str and len(value) == 0:
            return None
        if column == "year":
            if len(value) == 1:
                return int(value)
            if len(value) > 1:
                if value[0].isdigit():
                    return int(value[0])
                # Try second character.
                else:
                    return int(value[1])
        if column == "classe_letter":
            return value.lower()
        if column == "birth_date":
            if type(value) == int:
                # Ignore dummy values
                if value == 19000000:
                    return date.today()
                return date(year=int(str(value)[:4]),
                            month=int(str(value)[4:6]),
                            day=int(str(value)[6:]))

        return value

    def _sync(self, iterable) -> None:
        if not self.teaching:
            self.print_log("teaching is missing, aborting.")
            return
        processed = 0
        student_synced = set()
        if self.search_login_directory:
            self.ldap_connection = get_ldap_connection()
            self.base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
        self.print_log("Importing students…(%s)" % self.teaching.display_name)
        for entry in iterable:
            # First check mandatory field.
            matricule = int(self.get_value(entry, "matricule"))
            if not matricule:
                self.print_log("No matricule found, skipping student.")
                continue
            first_name = self.get_value(entry, "first_name")
            if not first_name:
                self.print_log("No first name found, skipping student.")
                continue
            last_name = self.get_value(entry, "last_name")
            if not last_name:
                self.print_log("No last name found, skipping student.")
                continue
            year = self.get_value(entry, "year")
            if not year:
                self.print_log("No year found, skipping student (%s %s)."
                               % (last_name, first_name))
                continue
            classe_letter = self.get_value(entry, "classe_letter")
            if not classe_letter:
                self.print_log("No classe letter found, skipping student (%s %s)."
                               % (last_name, first_name))
                continue
            try:
                student = StudentModel.objects.get(matricule=matricule)
                student.inactive_from = None
            except ObjectDoesNotExist:
                student = StudentModel(matricule=matricule)

            student.first_name = first_name
            student.last_name = last_name
            student.teaching = self.teaching

            # Check if student's classe already exists.
            try:
                classe = ClasseModel.objects.get(year=year,
                                                 letter=classe_letter,
                                                 teaching=self.teaching)
            except ObjectDoesNotExist:
                classe = ClasseModel(year=year,
                                     letter=classe_letter,
                                     teaching=self.teaching)
                classe.save()

            student.classe = classe

            courses = self.get_value(entry, "courses")
            if courses and type(courses) != list:
                courses = [courses]
            if courses:
                for c in courses:
                    try:
                        course_model = CourseModel.objects.get(id=c["id"])
                    except ObjectDoesNotExist:
                        course_model = CourseModel(id=c["id"], name=c["name"], teaching=self.teaching)
                        course_model.save()
                    try:
                        given_course = GivenCourseModel.objects.get(course=course_model, group=c["group"])
                    except ObjectDoesNotExist:
                        given_course = GivenCourseModel(course=course_model, group=c["group"])
                        given_course.save()
                    student.courses.add(given_course)
            student.save()

            student_synced.add(student.matricule)

            # Print progress.
            processed += 1
            if processed % 50 == 0:
                self.print_log(processed)

            # Additional info.
            try:
                info = student.additionalstudentinfo
            except ObjectDoesNotExist:
                info = AdditionalStudentInfo(student=student)
            for c in self.additional_columns:
                val = self.get_value(entry, c)
                if val:
                    setattr(info, c, val)
                else:
                    if c == "birth_date":
                        continue
                    setattr(info, c, "")
            if self.search_login_directory:
                self.ldap_connection.search(self.base_dn, "(matricule=%i)" % matricule, attributes='*')
                for r in self.ldap_connection.response:
                    ldap_info = get_django_dict_from_ldap(r)
                    info.username = ldap_info['username']
                    info.password = ldap_info['password']
            info.save()

        # Set inactives.
        self.print_log("Set inactive students…")
        all_students = StudentModel.objects.filter(teaching=self.teaching)
        for s in all_students:
            if s.matricule not in student_synced:
                s.inactive_from = timezone.make_aware(timezone.datetime.now())
                s.classe = None
                s.courses.clear()
                s.save()

        self.print_log("Import done.")


class ImportStudentCSV(ImportStudent):
    def __init__(self, teaching: TeachingModel, column_map: dict=None,
                 column_index: dict=None) -> None:
        super().__init__(teaching=teaching, search_login_directory=False)
        self.column_map = column_map
        if not column_index:
            self.column_to_index = {j: i for i, j in
                                    enumerate(["matricule", "last_name", "first_name",
                                               "year", "classe_letter"])}
        else:
            self.column_to_index = column_index

    def sync(self, text: TextIO, ignore_first_line: bool=False,
             has_header: bool=False) -> None:
        # First detect dialect.
        dialect = csv.Sniffer().sniff(text.readline())
        # Return to start.
        text.seek(0)

        reader = csv.reader(text, dialect)
        if ignore_first_line:
            next(reader, None)
        # Map column to row index with first line.
        if has_header:
            header = next(reader, None)
            if self.column_map:
                self.column_to_index = {self.column_map[j]: i for i, j in
                                        enumerate(header)}
            else:
                self.column_to_index = {j: i for i, j in
                                        enumerate(header)}

        super()._sync(reader)

    def get_value(self, entry: list, column: str) -> Union[int, str, date, None]:
        try:
            return self.format_value(entry[self.column_to_index[column]], column)
        except KeyError:
            return None


class ImportStudentLDAP(ImportStudent):
    def __init__(self, teaching: TeachingModel) -> None:
        super().__init__(teaching=teaching, search_login_directory=False)
        self.connection = get_ldap_connection()
        self.base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn

    def sync(self):
        self.connection.search(self.base_dn,
                               "(&(objectClass=eleve)(enseignement=%s))" % self.teaching.name,
                               attributes='*')
        ldap_entries = map(lambda entry: get_django_dict_from_ldap(entry), self.connection.response)
        super()._sync(ldap_entries)

    def get_value(self, entry: dict, column: str) -> Union[int, str, date, None]:
        if column == 'password':
            if '{SHA512}' in entry[column]:
                return 'Les données sensibles ne sont disponibles que sur https://local.isln.be'
        return super().get_value(entry, column)


class ImportStudentFDB(ImportStudent):
    column_map = {
        "last_name": "surname", "first_name": "firstname", "year": "classe_year",
        "doctor": "medecin", "doctor_phone": "medecin_phone", "mutual": "mutuelle",
        "medical_information": "medical_info",
        "street": "address", "locality": "city", "student_mobile": "student_gsm",
        "resp_last_name": "resp_surname", "resp_first_name": "resp_firstname",
        "resp_phone": "phone", "resp_mobile": "gsm", "resp_email": "email",
        "father_last_name": "father_surname", "father_first_name": "father_firstname", "father_mobile": "father_gsm",
        "mother_last_name": "mother_surname", "mother_first_name": "mother_firstname", "mother_mobile": "mother_gsm",
    }
    scholar_year = get_scholar_year()

    def __init__(self, teaching: TeachingModel, fdb_server, search_login_directory, teaching_type, classe_format="%C") -> None:
        super().__init__(teaching, search_login_directory)
        self.server = fdb_server
        self.teaching_type = teaching_type
        self.classe_format = classe_format

    def sync(self):
        from libreschoolfdb.reader import get_students
        self.print_log("Collecting students informations from ProEco database.")
        students = get_students(year=self.scholar_year, fdb_server=self.server,
                                teaching=self.teaching_type, absences_info=False,
                                classe_format=self.classe_format)
        # print(students)
        super()._sync(students.items())

    def get_value(self, entry: dict, column: str) -> Union[int, str, date, None]:
        if column == "matricule":
            return entry[0]
        elif column == "previous_class":
            if "previous_classe" in entry:
                return entry["previous_classe"]
            else:
                return None
        elif column == "username" or column == "password":
            return None
        elif column == "scholar_year":
            return self.scholar_year
        elif column in self.column_map:
            return entry[1][self.column_map[column]]
        else:
            return self.format_value(entry[1][column], column)
