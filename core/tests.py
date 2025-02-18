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

from datetime import date, datetime

from unittest.mock import patch, Mock

from django.test import TestCase
from django.contrib.auth.models import User
from .people import (
    People,
    STUDENT,
    get_years,
    get_classes,
    get_all_teachings,
    check_access_to_student,
    get_students_from_teacher,
)

from .utilities import in_scholar_year, get_scholar_year, extract_day_of_week

from .models import TeachingModel, StudentModel, ClasseModel, ResponsibleModel, CoreSettingsModel


class GetAllTeachingTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def test_get_all_teaching(self):
        teachings = get_all_teachings()
        self.assertListEqual(teachings, ["secondaire", "primaire"])


class PeopleTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def _assert_student_exist(self, student: StudentModel):
        self.assertIsNotNone(student)
        # student: StudentModel # Only supported in python 3.6
        self.assertEqual(student.first_name, "Guy")

    def _assert_teacher_exist(self, teacher: ResponsibleModel):
        self.assertIsNotNone(teacher)
        # teacher: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(teacher.first_name, "Jean")

    def _assert_educator_exist(self, educator: ResponsibleModel):
        self.assertIsNotNone(educator)
        # educator: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(educator.first_name, "Audrey")

    def _assert_responsible_exist(self, responsible: ResponsibleModel):
        self.assertIsNotNone(responsible)
        # responsible: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(responsible.first_name, "Jean")

    def test_get_person(self):
        student = People().get_person(
            person_type="student", person_id=1000, teaching=["secondaire"]
        )
        self._assert_student_exist(student)
        # Check that it doesn't depend on teaching.
        self.assertEqual(student, People().get_person(person_type="student", person_id=1000))
        teacher = People().get_person(
            person_type="teacher", person_id=100003, teaching=["secondaire"]
        )
        self._assert_teacher_exist(teacher)
        educator = People().get_person(
            person_type="educator", person_id=100002, teaching=["secondaire"]
        )
        self._assert_educator_exist(educator)

    def test_get_student(self):
        student = People().get_student_by_id(person_id=1000)
        self._assert_student_exist(student)
        other_student = People().get_student_by_id(person_id=4242)
        self.assertIsNone(other_student)

    def test_get_teacher(self):
        teacher = People().get_teacher_by_id(person_id=100003)
        self._assert_teacher_exist(teacher)

        teacher = People().get_teacher_by_id(person_id=100003, teaching=["secondaire"])
        self._assert_teacher_exist(teacher)
        other_teacher = People().get_teacher_by_id(person_id=1234, teaching=["secondaire"])
        self.assertIsNone(other_teacher)
        other_teacher = People().get_teacher_by_id(person_id=100003, teaching=["primaire"])
        self.assertIsNone(other_teacher)

    def test_get_educator(self):
        educator = People().get_educator_by_id(person_id=100002)
        self._assert_educator_exist(educator)

        educator = People().get_educator_by_id(person_id=100002, teaching=["secondaire"])
        self._assert_educator_exist(educator)
        educator = People().get_educator_by_id(person_id=1, teaching=["secondaire"])
        self.assertIsNone(educator)

    def test_get_responsible(self):
        responsible = People().get_responsible_by_id(person_id=1)
        self._assert_responsible_exist(responsible)

        responsible = People().get_responsible_by_id(person_id=1, teaching=["secondaire"])
        self._assert_responsible_exist(responsible)
        educator = People().get_responsible_by_id(person_id=100002, teaching=["secondaire"])
        self._assert_educator_exist(educator)
        teacher = People().get_responsible_by_id(person_id=100003, teaching=["secondaire"])
        self._assert_teacher_exist(teacher)

        responsible = People().get_responsible_by_id(person_id=9999, teaching=["secondaire"])
        self.assertIsNone(responsible)

    def test_get_people_by_name_by_model(self):
        result = People()._get_people_by_name_by_model(StudentModel, "Adelai")
        self.assertGreater(len(result[0]), 0)

        self.assertEqual(type(result[0][0]), StudentModel)
        result = People()._get_people_by_name_by_model(
            StudentModel, "Adelai", teaching=["secondaire"]
        )
        self.assertEqual(len(result[0]), 4)

        result = People()._get_people_by_name_by_model(
            StudentModel, "Barre Adelai", teaching=["secondaire"]
        )
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(type(result[0][0]), StudentModel)

        teaching_secondaire = TeachingModel.objects.filter(name="secondaire")
        result = People()._get_people_by_name_by_model(
            StudentModel, "Barre Adelai", teaching=teaching_secondaire
        )
        self.assertEqual(len(result[0]), 1)

    def test_get_people_by_name(self):
        result = People().get_people_by_name(name="jacquel")
        self.assertEqual(len(result["student"][0]) + len(result["responsible"][0]), 6)

        result = People().get_people_by_name(name="jacquel", person_type=STUDENT)
        self.assertEqual(len(result), 5)

        result = People().get_people_by_name(name="jacqueline dan")
        self.assertEqual(len(result["student"][0]) + len(result["responsible"][0]), 1)

        result = People().get_people_by_name(name="jacquel", teaching=["all"])
        self.assertEqual(len(result["student"][0]) + len(result["responsible"][0]), 6)
        result = People().get_people_by_name(name="jacquel", teaching=["primaire"])
        self.assertEqual(len(result["student"][0]) + len(result["responsible"][0]), 1)

    def test_get_students_by_name(self):
        result = People().get_students_by_name("Adelaï")
        self.assertEqual(result.count(), 8)
        result = People().get_students_by_name("zzz")
        self.assertEqual(result.count(), 0)

    def test_get_students_by_name_with_classes(self):
        classe_1A = ClasseModel.objects.filter(year=1, letter="A", teaching__id=1)
        classe_3B = ClasseModel.objects.filter(year=3, letter="B", teaching__id=2)
        classe_6B = ClasseModel.objects.filter(year=6, letter="C", teaching__id=1)
        result = People().get_students_by_name("Adelaï", classes=classe_1A)
        self.assertEqual(result.count(), 1)
        result = People().get_students_by_name("Adelaï", classes=classe_3B | classe_1A)
        self.assertEqual(result.count(), 2)
        result = People().get_students_by_name("Jean Dupont", classes=classe_6B)
        self.assertEqual(result.count(), 0)

    def test_get_teachers_by_name(self):
        result = People().get_teachers_by_name("Jean Chev")
        self.assertEqual(result.count(), 1)
        result = People().get_teachers_by_name("Jean Dupont")
        self.assertEqual(result.count(), 0)

    def test_get_educators_by_name(self):
        result = People().get_educators_by_name("Hoareau")
        self.assertEqual(result.count(), 1)
        result = People().get_educators_by_name("Jean Chevalier")
        self.assertEqual(result.count(), 0)

    def test_get_responsibles_by_name(self):
        result = People().get_responsibles_by_name("Jean")
        self.assertEqual(result.count(), 3)
        result = People().get_responsibles_by_name("Jésus")
        self.assertEqual(len(result), 0)

    def test_get_students_by_classe(self):
        result = People().get_students_by_classe("1")
        self.assertEqual(result.count(), 210)
        result = People().get_students_by_classe("1A")
        self.assertEqual(result.count(), 30)
        result_lower_case = People().get_students_by_classe("1a")
        self.assertEqual(result.count(), result_lower_case.count())

        teaching_secondaire = TeachingModel.objects.filter(name="secondaire")
        teaching_primaire = TeachingModel.objects.filter(name="primaire")
        result = People().get_students_by_classe("1", teaching=teaching_secondaire)
        self.assertEqual(result.count(), 105)
        result = People().get_students_by_classe("1A", teaching=("secondaire",))
        self.assertEqual(result.count(), 15)
        result = People().get_students_by_classe("1z", teaching=teaching_primaire)
        self.assertEqual(result.count(), 0)

        result = People().get_students_by_classe("")
        self.assertEqual(result.count(), 0)

        result = People().get_students_by_classe("a")
        self.assertEqual(result.count(), 0)

        classe = ClasseModel.objects.get(
            year=1, letter__iexact="a", teaching=teaching_secondaire.first()
        )
        result = People().get_students_by_classe(classe)
        self.assertEqual(result.count(), 15)

        result = People().get_students_by_classe(None)
        self.assertEqual(result.count(), 0)


class AccessTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username="director")
        # Get a student user.
        self.student_user = User.objects.get(username="student")
        # Get a teacher user.
        self.teacher_user = User.objects.get(username="teacher")
        # Get an educator user.
        self.educator_user = User.objects.get(username="educator")
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username="coordonator")


class GetClassesTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username="director")
        # Get a student user.
        self.student_user = User.objects.get(username="student")
        # Get a teacher user.
        self.teacher_user = User.objects.get(username="teacher")
        # Get an educator user.
        self.educator_user = User.objects.get(username="educator")
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username="coordonator")

    def test_teaching(self):
        classes = get_classes([])
        self.assertListEqual(list(classes), [])

        classes = get_classes(["all"])
        self.assertEqual(classes.count(), 84)

        classes = get_classes(["primaire"])
        self.assertEqual(classes.count(), 42)

        teaching_primaire = TeachingModel.objects.filter(name="primaire")
        classes = get_classes(teaching=teaching_primaire)
        self.assertEqual(classes.count(), 42)

    def test_direction_access(self):
        classes = get_classes(["primaire", "secondaire"], check_access=True, user=self.dir_user)
        self.assertEqual(classes.count(), 42)

        # The following parameters should not change the results.
        classes = get_classes(
            ["primaire", "secondaire"],
            check_access=True,
            user=self.dir_user,
            tenure_class_only=False,
        )
        self.assertEqual(classes.count(), 42)
        classes = get_classes(
            ["primaire", "secondaire"], check_access=True, user=self.dir_user, educ_by_years=False
        )
        self.assertEqual(classes.count(), 42)

    def test_student_access(self):
        classes = get_classes(check_access=True, user=self.student_user)
        self.assertEqual(classes.count(), 0)

    def test_teacher_access(self):
        classes = get_classes(check_access=True, user=self.teacher_user, tenure_class_only=True)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["1D"])
        classes = get_classes(check_access=True, user=self.teacher_user, tenure_class_only=False)
        self.assertEqual(classes.count(), 5)

        teaching_secondaire = TeachingModel.objects.filter(name="secondaire")
        classes = get_classes(
            teaching=teaching_secondaire, check_access=True, user=self.teacher_user
        )
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["1D"])

    def test_educator_access(self):
        classes = get_classes(check_access=True, user=self.educator_user)
        self.assertEqual(classes.count(), 14)

        classes = get_classes(check_access=True, user=self.educator_user, educ_by_years=False)
        self.assertEqual(classes.count(), 4)

    def test_coordonator_access(self):
        # It is a 1, 2, 3 year coordonator so it has all classes in the first, second and third year in
        # secondaire.
        classes = get_classes(check_access=True, user=self.coordonator_user)
        self.assertEqual(classes.count(), 21)


class GetYearsTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username="director")
        # Get a student user.
        self.student_user = User.objects.get(username="student")
        # Get a teacher user.
        self.teacher_user = User.objects.get(username="teacher")
        # Get an educator user.
        self.educator_user = User.objects.get(username="educator")
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username="coordonator")

    def test_teaching(self):
        years = get_years(teaching=["all"])
        self.assertSetEqual(years, {1, 2, 3, 4, 5, 6})

        years = get_years(teaching=TeachingModel.objects.all())
        self.assertSetEqual(years, {1, 2, 3, 4, 5, 6})

        years = get_years(teaching=("primaire",))
        self.assertSetEqual(years, {1, 2, 3, 4, 5, 6})

    def test_direction_access(self):
        years = get_years(check_access=True, user=self.dir_user)
        self.assertSetEqual(years, {1, 2, 3, 4, 5, 6})

    def test_student_access(self):
        years = get_years(check_access=True, user=self.student_user)
        self.assertSetEqual(years, set())

    def test_teacher_access(self):
        years = get_years(check_access=True, user=self.teacher_user)
        self.assertSetEqual(years, {1})
        years = get_years(check_access=True, user=self.teacher_user, tenure_class_only=False)
        self.assertSetEqual(years, {1, 5, 6})

    def test_educator_access(self):
        years = get_years(check_access=True, user=self.educator_user)
        self.assertSetEqual(years, {5, 6})
        years = get_years(check_access=True, user=self.educator_user, educ_by_years=False)
        self.assertSetEqual(years, {2, 3, 6})

    def test_coordonator_access(self):
        years = get_years(check_access=True, user=self.coordonator_user)
        self.assertSetEqual(years, {1, 2, 3})


class CheckAccessToStudentTest(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username="director")
        # Get a student user.
        self.student_user = User.objects.get(username="student")
        # Get a teacher user.
        # Classes (secondaire): [1C, 5D, 5G, 6C]
        # Tenure (secondaire): [1D]
        self.teacher_user = User.objects.get(username="teacher")
        # Get an educator user.
        # Classes (secondaire): [2D, 3B, 6C, 6F]
        # Years: [5, 6, 7]
        self.educator_user = User.objects.get(username="educator")
        # Get a coordonator user.
        self.coordinator_user = User.objects.get(username="coordonator")
        # Years: [1, 2, 3]

        # Get students to test on.
        self.student_one_a_secondaire = StudentModel.objects.get(matricule=1010)
        self.student_one_c_secondaire = StudentModel.objects.get(matricule=1034)
        self.student_one_d_secondaire = StudentModel.objects.get(matricule=1047)
        self.student_two_d_secondaire = StudentModel.objects.get(matricule=1152)
        self.student_five_a_secondaire = StudentModel.objects.get(matricule=1433)
        self.student_six_a_secondaire = StudentModel.objects.get(matricule=1538)

    def test_student_access(self):
        has_access = check_access_to_student(self.student_one_d_secondaire, self.student_user)
        self.assertFalse(has_access)

    def test_teacher_access(self):
        # Teacher should have access as it is the tenure.
        has_access = check_access_to_student(self.student_one_d_secondaire, self.teacher_user)
        self.assertTrue(has_access)
        # Student from another classe.
        has_access = check_access_to_student(self.student_one_a_secondaire, self.teacher_user)
        self.assertFalse(has_access)
        # With all classes.
        has_access = check_access_to_student(
            self.student_one_c_secondaire,
            self.teacher_user,
            tenure_class_only=False,
        )
        self.assertTrue(has_access)
        # With all classes.
        has_access = check_access_to_student(
            self.student_five_a_secondaire,
            self.teacher_user,
            tenure_class_only=False,
        )
        self.assertFalse(has_access)

    def test_educator_access(self):
        # Educator should have access to its years.
        has_access = check_access_to_student(self.student_six_a_secondaire, self.educator_user)
        self.assertTrue(has_access)
        has_access = check_access_to_student(self.student_one_a_secondaire, self.educator_user)
        self.assertFalse(has_access)

        # Check access by classes.
        has_access = check_access_to_student(
            self.student_two_d_secondaire, self.educator_user, educ_by_years=False
        )
        self.assertTrue(has_access)
        has_access = check_access_to_student(
            self.student_six_a_secondaire, self.educator_user, educ_by_years=False
        )
        self.assertFalse(has_access)

    def test_coordinator_access(self):
        # Coordinator should have access to its years.
        has_access = check_access_to_student(self.student_one_a_secondaire, self.coordinator_user)
        self.assertTrue(has_access)
        has_access = check_access_to_student(self.student_six_a_secondaire, self.coordinator_user)
        self.assertFalse(has_access)

    def test_director_access(self):
        # Director should have access to all students.
        students = [
            self.student_one_a_secondaire,
            self.student_one_c_secondaire,
            self.student_one_d_secondaire,
            self.student_two_d_secondaire,
            self.student_five_a_secondaire,
            self.student_six_a_secondaire,
        ]
        has_access = [check_access_to_student(s, self.dir_user) for s in students]
        self.assertListEqual(has_access, [True, True, True, True, True, True])


class CheckStudentTeacherRelationship(TestCase):
    fixtures = ["base_random_people_auth.json", "base_random_people_core"]

    def test_get_students_from_teacher(self):
        # Get Noel Etienne who has english (abc) (thus 1A, 1B, 1C) course
        # and 1E tenure and 2B, 4B and 4D classes.
        teacher = ResponsibleModel.objects.get(pk=6)
        # Default settings is BY_CLASSES thus 45 + 15 students.
        students = get_students_from_teacher(teacher)
        self.assertEqual(students.count(), 60)
        # Use BY_COURSES setting.
        settings = CoreSettingsModel.objects.first()
        settings.student_teacher_relationship = CoreSettingsModel.BY_COURSES
        settings.save()
        students = get_students_from_teacher(teacher)
        self.assertEqual(students.count(), 45)
        # Use BY_CLASSES_COURSES
        settings.student_teacher_relationship = CoreSettingsModel.BY_CLASSES_COURSES
        settings.save()
        students = get_students_from_teacher(teacher)
        self.assertEqual(students.count(), 105)


# Mocking the get_scholar_year and get_settings functions for testing purposes
def mock_get_scholar_year():
    return 2023


def mock_get_settings():
    return CoreSettingsModel(month_scholar_year_start=9, day_scholar_year_start=1)


@patch("core.utilities.get_scholar_year", return_value=2023)
@patch(
    "core.views.get_core_settings",
    return_value=CoreSettingsModel(month_scholar_year_start=9, day_scholar_year_start=1),
)
class TestInScholarYear(TestCase):
    def test_in_scholar_year_happy_path(self, mock_get_settings, mock_get_scholar_year):
        # Test cases for the happy path
        self.assertTrue(in_scholar_year(date(2023, 10, 1)))  # After start date in current year
        self.assertTrue(in_scholar_year(date(2024, 8, 31)))  # Before start date in next year
        self.assertFalse(in_scholar_year(date(2022, 9, 1)))  # Before start date in previous year

    def test_in_scholar_year_edge_cases(self, mock_get_settings, mock_get_scholar_year):
        # Test cases for edge cases
        self.assertTrue(in_scholar_year(date(2023, 9, 1)))  # Start date of the scholar year
        self.assertFalse(
            in_scholar_year(date(2023, 8, 31))
        )  # Day before start date in current year
        self.assertFalse(in_scholar_year(date(2024, 9, 1)))  # Start date of the next scholar year
        self.assertTrue(in_scholar_year(date(2024, 8, 31)))  # Day before start date in next year


@patch("core.views.timezone.now")
@patch(
    "core.views.get_core_settings",
    return_value=CoreSettingsModel(month_scholar_year_start=9, day_scholar_year_start=1),
)
class TestGetScholarYear(TestCase):

    def test_happy_path(self, mock_get_settings, mock_now):
        # Set up the mock to return a date after the start of the scholar year
        mock_now.return_value = datetime(2023, 10, 15)

        # Call the function and check if it returns the correct year
        result = get_scholar_year()
        self.assertEqual(result, 2023)

    def test_before_start_of_scholar_year(self, mock_get_settings, mock_now):
        # Set up the mock to return a date before the start of the scholar year
        mock_now.return_value = datetime(2023, 8, 14)

        # Call the function and check if it returns the correct year (previous year)
        result = get_scholar_year()
        self.assertEqual(result, 2022)

    def test_on_start_of_scholar_year(self, mock_get_settings, mock_now):
        # Set up the mock to return a date exactly at the start of the scholar year
        mock_now.return_value = datetime(2023, 9, 1)

        # Call the function and check if it returns the correct year (current year)
        result = get_scholar_year()
        self.assertEqual(result, 2023)

    def test_just_before_start_of_scholar_year(self, mock_get_settings, mock_now):
        # Set up the mock to return a date just before the start of the scholar year
        mock_now.return_value = datetime(2023, 8, 30)

        # Call the function and check if it returns the correct year (previous year)
        result = get_scholar_year()
        self.assertEqual(result, 2022)


class TestExtractDayOfWeek(TestCase):

    def test_happy_path(self):
        self.assertEqual(extract_day_of_week("1,3,5"), [1, 3, 5])
        self.assertEqual(extract_day_of_week("2-4"), [2, 3, 4])
        self.assertEqual(extract_day_of_week("1-3,5-7"), [1, 2, 3, 5, 6, 7])

    def test_range_with_single_digit(self):
        self.assertEqual(extract_day_of_week("1-3,5"), [1, 2, 3, 5])
        self.assertEqual(extract_day_of_week("1-2,4"), [1, 2, 4])

    def test_empty_string(self):
        self.assertEqual(extract_day_of_week(""), [])

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            extract_day_of_week("1-3,5-2")

    def test_non_digit_characters(self):
        with self.assertRaises(ValueError):
            extract_day_of_week("a,b,c")
        with self.assertRaises(ValueError):
            extract_day_of_week("1,a,3")

    def test_duplicate_days(self):
        self.assertEqual(extract_day_of_week("1,1,1"), [1])
        self.assertEqual(extract_day_of_week("1-2,1-3"), [1, 2, 3])

    def test_large_range(self):
        self.assertEqual(extract_day_of_week("1-7"), list(range(1, 8)))
