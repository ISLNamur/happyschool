import itertools

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .people import People, get_default_teaching, STUDENT, get_years, get_classes,\
    get_years

from .models import TeachingModel, StudentModel, ClasseModel, ResponsibleModel


class GetDefaultTeachingTest(TestCase):
    def test_with_none(self):
        teaching = get_default_teaching()
        self.assertListEqual(teaching, [])

    def test_with_one_default(self):
        TeachingModel.objects.create(name="secondaire",
                                     display_name="Secondaire",
                                     default=True)
        self.assertEqual(get_default_teaching(), ["secondaire"])

    def test_with_two_default(self):
        TeachingModel.objects.create(name="secondaire",
                                     display_name="Secondaire",
                                     default=True)
        TeachingModel.objects.create(name="primaire",
                                     display_name="Primaire",
                                     default=True)
        self.assertListEqual(get_default_teaching(), ["secondaire", "primaire"])


class PeopleTest(TestCase):
    fixtures = ['test_core.json']

    def _assert_student_exist(self, student: object):
        self.assertIsNotNone(student)
        # student: StudentModel # Only supported in python 3.6
        self.assertEqual(student.first_name, "Toto")

    def _assert_teacher_exist(self, teacher: object):
        self.assertIsNotNone(teacher)
        # teacher: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(teacher.first_name, "Tea")

    def _assert_educator_exist(self, educator: object):
        self.assertIsNotNone(educator)
        # educator: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(educator.first_name, "Tedu")

    def _assert_responsible_exist(self, responsible):
        self.assertIsNotNone(responsible)
        # responsible: ResponsibleModel # Only supported in python 3.6
        self.assertEqual(responsible.first_name, "Trespon")

    def test_get_person(self):
        student = People().get_person(person_type='student',
                                      person_id=1234,
                                      teaching=['secondaire'])
        self._assert_student_exist(student)
        # Check that it doesn't depend on teaching.
        self.assertEqual(student, People().get_person(person_type='student',
                                                      person_id=1234))
        teacher = People().get_person(person_type='teacher',
                                      person_id=123,
                                      teaching=['secondaire'])
        self._assert_teacher_exist(teacher)
        educator = People().get_person(person_type='educator',
                                       person_id=12,
                                       teaching=['secondaire'])
        self._assert_educator_exist(educator)

    def test_get_student(self):
        student = People().get_student_by_id(person_id=1234)
        self._assert_student_exist(student)
        other_student = People().get_student_by_id(person_id=4242)
        self.assertIsNone(other_student)

    def test_get_teacher(self):
        teacher = People().get_teacher_by_id(person_id=123,
                                                teaching=['secondaire'])
        self._assert_teacher_exist(teacher)
        other_teacher = People().get_teacher_by_id(person_id=1234,
                                                      teaching=['secondaire'])
        self.assertIsNone(other_teacher)
        other_teacher = People().get_teacher_by_id(person_id=123,
                                                      teaching=['primaire'])
        self.assertIsNone(other_teacher)

    def test_get_educator(self):
        educator = People().get_educator_by_id(person_id=12,
                                                  teaching=['secondaire'])
        self._assert_educator_exist(educator)
        educator = People().get_educator_by_id(person_id=1,
                                                  teaching=['secondaire'])
        self.assertIsNone(educator)

    def test_get_responsible(self):
        responsible = People().get_responsible_by_id(person_id=1,
                                                        teaching=['secondaire'])
        self._assert_responsible_exist(responsible)
        educator = People().get_responsible_by_id(person_id=12,
                                                     teaching=['secondaire'])
        self._assert_educator_exist(educator)
        teacher = People().get_responsible_by_id(person_id=123,
                                                    teaching=['secondaire'])
        self._assert_teacher_exist(teacher)

        responsible = People().get_responsible_by_id(person_id=9999,
                                                        teaching=['secondaire'])
        self.assertIsNone(responsible)

    def test_get_people_by_name_by_model(self):
        result = People()._get_people_by_name_by_model(StudentModel, "tot")
        self.assertGreater(len(result), 0)
        self.assertEqual(type(result[0]), StudentModel)
        result = People()._get_people_by_name_by_model(StudentModel, "tot",
                                                          teaching=['secondaire'])
        self.assertEqual(len(result), 1)

    def test_get_people_by_name(self):
        result = People().get_people_by_name(name="t")
        self.assertEqual(len(result), 5)

        result = People().get_people_by_name(name="t", person_type=STUDENT)
        self.assertEqual(len(result), 2)

        result = People().get_people_by_name(name="tea")
        self.assertEqual(len(result), 1)

        result = People().get_people_by_name(name="t", teaching=['all'])
        self.assertEqual(len(result), 5)
        result = People().get_people_by_name(name="t", teaching=['primaire'])
        self.assertEqual(len(result), 1)

    def test_get_students_by_name(self):
        result = People().get_students_by_name("t")
        self.assertEqual(len(result), 2)
        result = People().get_students_by_name("a")
        self.assertEqual(len(result), 0)

    def test_get_students_by_name_with_classes(self):
        classe_1A = ClasseModel.objects.filter(year=1, letter="a")
        classe_3B = ClasseModel.objects.filter(year=3, letter="b")
        classe_6B = ClasseModel.objects.filter(year=6, letter="B")
        result = People().get_students_by_name("t", classes=classe_1A)
        self.assertEqual(len(result), 1)
        result = People().get_students_by_name("t", classes=classe_3B | classe_1A)
        self.assertEqual(len(result), 1)
        result = People().get_students_by_name("t", classes=classe_6B)
        self.assertEqual(len(result), 0)

    def test_get_teachers_by_name(self):
        result = People().get_teachers_by_name("tea")
        self.assertEqual(len(result), 1)
        result = People().get_teachers_by_name("a")
        self.assertEqual(len(result), 0)

    def test_get_educators_by_name(self):
        result = People().get_educators_by_name("ted")
        self.assertEqual(len(result), 1)
        result = People().get_educators_by_name("a")
        self.assertEqual(len(result), 0)

    def test_get_responsibles_by_name(self):
        result = People().get_responsibles_by_name("tre")
        self.assertEqual(len(result), 1)
        result = People().get_responsibles_by_name("t")
        self.assertEqual(len(result), 3)
        result = People().get_responsibles_by_name("a")
        self.assertEqual(len(result), 0)


class AccessTest(TestCase):
    fixtures = ['test_core.json']

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username='director')
        # Get a student user.
        self.student_user = User.objects.get(username='student')
        # Get a teacher user.
        self.teacher_user = User.objects.get(username='teacher')
        # Get an educator user.
        self.educator_user = User.objects.get(username='educator')
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username='coordonator')


class GetClassesTest(TestCase):
    fixtures = ['test_core.json']

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username='director')
        # Get a student user.
        self.student_user = User.objects.get(username='student')
        # Get a teacher user.
        self.teacher_user = User.objects.get(username='teacher')
        # Get an educator user.
        self.educator_user = User.objects.get(username='educator')
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username='coordonator')

    def test_default(self):
        # teaching default is secondaire.
        classes = get_classes()
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["1A", "1B"])

    def test_teaching(self):
        classes = get_classes(["all"])
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["1A", "1B", "3B"])

        classes = get_classes(["primaire"])
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["3B"])

    def test_direction_access(self):
        classes = get_classes(["primaire", "secondaire"], check_access=True, user=self.dir_user)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ["1A", "1B"])

    def test_student_access(self):
        classes = get_classes(check_access=True, user=self.student_user)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, [])

    def test_teacher_access(self):
        classes = get_classes(check_access=True, user=self.teacher_user)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ['1B'])

    def test_educator_access(self):
        classes = get_classes(check_access=True, user=self.educator_user)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(classes, ['1A', '1B'])

    def test_coordonator_access(self):
        # It is a 1 year coordonator so it has all classes in the first year in secondaire.
        classes = get_classes(check_access=True, user=self.coordonator_user)
        classes = list(map(lambda c: c.compact_str, classes))
        self.assertListEqual(sorted(classes), ['1A', '1B'])


class GetYearsTest(TestCase):
    fixtures = ['test_core.json']

    def setUp(self):
        # Get a direction user.
        self.dir_user = User.objects.get(username='director')
        # Get a student user.
        self.student_user = User.objects.get(username='student')
        # Get a teacher user.
        self.teacher_user = User.objects.get(username='teacher')
        # Get an educator user.
        self.educator_user = User.objects.get(username='educator')
        # Get a coordonator user.
        self.coordonator_user = User.objects.get(username='coordonator')

    def test_default(self):
        years = get_years()
        self.assertSetEqual(years, {1})

    def test_teaching(self):
        years = get_years(teaching=["all"])
        self.assertSetEqual(years, {1, 3})

    def test_direction_access(self):
        years = get_years(check_access=True, user=self.dir_user)
        self.assertSetEqual(years, {1})

    def test_student_access(self):
        years = get_years(check_access=True, user=self.student_user)
        self.assertSetEqual(years, set())

    def test_teacher_access(self):
        years = get_years(check_access=True, user=self.teacher_user)
        self.assertSetEqual(years, set())

    def test_educator_access(self):
        years = get_years(check_access=True, user=self.educator_user)
        self.assertSetEqual(years, {1})

    def test_coordonator_access(self):
        years = get_years(check_access=True, user=self.coordonator_user)
        self.assertSetEqual(years, {1})


# class getStudentsClassesTest(TestCase):
#     fixtures = ['test_core.json']
#
#     def test_default(self):
#         classes = get_student_classes("")
#         self.assertListEqual(classes, ['1A – Secondaire', '3B – Primaire'])
#
#     def test_one_year(self):
#         classes = get_student_classes("1")
#         self.assertListEqual(classes, ['1A – Secondaire'])
#         classes = get_student_classes("3")
#         self.assertListEqual(classes, ['3B – Primaire'])
#
#     def test_one_classe(self):
#         classes = get_student_classes("1A")
#         self.assertListEqual(classes, ['1A – Secondaire'])
#
#     def test_teaching(self):
#         classes = get_student_classes("3B", ["secondaire"])
#         self.assertListEqual(classes, ['3B – Primaire'])
#
#
# class getStudentsYearsTest(TestCase):
#     fixtures = ['test_core.json']
#
#     def test_default(self):
#         years = get_students_years("")
#         self.assertListEqual(years, ['1ères', '3èmes'])
#
#     def test_one_year(self):
#         years = get_students_years("1")
#         self.assertListEqual(years, ['1ères'])
#         years = get_students_years("1e")
#         self.assertListEqual(years, ['1ères'])
#
#     def test_teaching(self):
#         years = get_students_years("3", ["secondaire"])
#         self.assertListEqual(years, ['3èmes'])
#
#
# class getStudentsClassesYears(TestCase):
#     fixtures = ['test_core.json']
#
#     def test_default(self):
#         classes_years = get_students_classes_years("")
#         self.assertSetEqual(set(classes_years), {"1A – Secondaire", "1ères", "3B – Primaire", "3èmes"})
