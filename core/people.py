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

import itertools
from unidecode import unidecode
from typing import Union

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q, QuerySet, Model
from django.db.utils import OperationalError, ProgrammingError

from .models import ResponsibleModel, StudentModel, TeachingModel, ClasseModel, CoreSettingsModel

# Person type:
STUDENT = 'student'
TEACHER = 'teacher'
EDUCATOR = 'educator'
RESPONSIBLE = 'responsible'
ALL = 'all'


def get_all_teachings():
    return list(map(lambda t: t[0], TeachingModel.objects.all().values_list("name")))


def get_core_settings():
    settings_model = CoreSettingsModel.objects.first()
    if not settings_model:
        # Create default settings.
        settings_model = CoreSettingsModel()
        settings_model.save()
    return settings_model


class People:
    """
    Class that handles people search and access.
    """

    def get_person(self,
                   teaching: list=('all',),
                   person_type=ALL,
                   **kwargs) -> object:
        """
        Get the first person from the given arguments.
        :param teaching: The teaching of the person.
        :param person_type: The person's type (student, teacher,…).
        :return: The related model object or None if no one is found.
        :rtype: dict
        """

        function_person = "get_%s" % person_type if person_type != ALL else 'person'

        if 'person_id' in kwargs:
            get_by_id = getattr(self, function_person + "_by_id", None)
            kwargs['teaching'] = teaching
            return get_by_id(**kwargs)

    @staticmethod
    def get_teacher_by_id(person_id: int,
                          teaching: list=('all',)) -> object:
        """
        Get a teacher by specifying an id and the teaching.
        :param person_id:  The teacher's id.
        :param teaching: A list of teachers' teachings.
        :return: A TeacherModel object or None.
        """
        try:
            if 'all' in teaching:
                return ResponsibleModel.objects.get(matricule=person_id,
                                                    is_teacher=True)

            return ResponsibleModel.objects.get(matricule=person_id,
                                                teaching__name__in=teaching,
                                                is_teacher=True)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_educator_by_id(person_id: int,
                           teaching: list=('all',)) -> object:
        """
        Get a educator by specifying an id and the teaching.
        :param person_id:  The educator's id.
        :param teaching: A list of educators' teachings.
        :return: A EducatorModel object.
        """
        try:
            if 'all' in teaching:
                return ResponsibleModel.objects.get(matricule=person_id,
                                                    is_educator=True)

            return ResponsibleModel.objects.get(matricule=person_id,
                                                teaching__name__in=teaching,
                                                is_educator=True)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_student_by_id(person_id: int,
                          teaching: list=('all',)) -> object:
        """
        Get a student by specifying an id. We assume that the id unique among
        different teachings.
        :param person_id:  The student's id.
        :param teaching: A list of students' teachings.
        :return: A StudentModel object.
        """
        try:
            if 'all' in teaching:
                return StudentModel.objects.get(matricule=person_id)

            return StudentModel.objects.get(matricule=person_id, teaching__name__in=teaching)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_responsible_by_id(person_id: int,
                              teaching: list=('all',)) -> object:
        """
        Get a responsible (educator, teacher or a responsible object) by
        specifying an id and the teaching. It will first look at non teachers
        and non educators, then educators and finally teachers.
        :param person_id:  The responsible's id.
        :param teaching: A list of responsibles' teachings.
        :return: A EducatorModel object.
        """
        params = {'matricule': person_id}
        if 'all' not in teaching:
            params['teaching__name__in'] = teaching

        try:
            return ResponsibleModel.objects.get(**params)
        except ObjectDoesNotExist:
            return None

    def get_people_by_name(self,
                           name: str,
                           teaching: list=('all',),
                           classes: list=None,
                           person_type=ALL,
                           active: bool=True) -> dict:
        """
        Get people by their name.
        :param name: String that starts the people's name.
        :param teaching: A list of the person's teachings.
        :param classes: A ClasseModel queryset to filter students by classes.
        :param person_type: People's type (students, educators,…).
        :param active: Filter out inactive people.
        :return: A list of Queryset.
        """

        if person_type != ALL:
            get_by_name = getattr(self, "get_%ss_by_name" % person_type, None)
            return get_by_name(name=name, teaching=teaching, active=active)


        students = self._get_people_by_name_by_model(StudentModel, name=name, teaching=teaching, active=active)
        responsibles = self._get_people_by_name_by_model(ResponsibleModel, name=name, teaching=teaching, active=active)

        return {'student': students, 'responsible': responsibles}

    @staticmethod
    def _get_people_by_name_by_model(model_name: Model,
                                     name: str,
                                     teaching: list=('all',),
                                     active: bool = True,
                                     additional_filter: dict={}) -> (QuerySet, int):
        """
        Private method where you can get people by their name and specify the
        model object you expect to have.
        :param model_name: People's model.
        :param name: String that starts the teachers' name.
        :param active: Filter out inactive people.
        :param teaching: A list of teachers' teachings.
        :return: A QuerySet of teachers.
        """
        tokens = name.split(" ")
        people = model_name.objects.none()
        quality = 2

        if len(tokens) > 1:
            # First check compound last name.
            people = model_name.objects.filter(Q(last_name__unaccent__istartswith=" ".join(tokens[:2]))
                                               | Q(last_name__unaccent__istartswith=" ".join(tokens[-2:])))
            if len(people) == 0:
                people = model_name.objects.filter(Q(first_name__unaccent__iexact=tokens[0], last_name__unaccent__istartswith=tokens[1])
                                               | Q(first_name__unaccent__istartswith=tokens[1], last_name__unaccent__iexact=tokens[0]))

        if len(people) == 0:
            quality = 1
            for name_part in tokens:
                people |= model_name.objects.filter(Q(first_name__unaccent__istartswith=name_part)
                                                   | Q(last_name__unaccent__istartswith=name_part))

        if teaching and 'all' not in teaching:
            if type(teaching[0]) == TeachingModel:
                people = people.filter(teaching__in=teaching)
            else:
                people = people.filter(teaching__name__in=teaching)

        if active:
            people = people.filter(inactive_from__isnull=True)
        if additional_filter:
            people = people.filter(**additional_filter)

        return (people, quality)

    def get_students_by_name(self, name: str,
                             teaching: list=('all',),
                             classes: list=None,
                             active: bool=True) -> QuerySet:
        """
        Get students by their name.
        :param name: String that starts the students' name.
        :param teaching: A list of students' teachings.
        :param classes: A ClasseModel queryset.
        :param active: Filter out inactive students.
        :return: A QuerySet of students.
        """
        students = self._get_people_by_name_by_model(StudentModel,
                                                     name=name,
                                                     teaching=teaching,
                                                     active=active)[0]
        if type(classes) == QuerySet:
            students = students.filter(classe__id__in=classes.values_list("id"))

        return students

    def get_teachers_by_name(self,
                             name: str,
                             teaching: list=('all',),
                             active: bool=True) -> QuerySet:
        """
        Get teachers by their name.
        :param name: String that starts the teachers' name.
        :param teaching: A list of teachers' teachings.
        :param active: Filter out inactive teachers.
        :return: A QuerySet of teachers.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching,
                                                 active=active,
                                                 additional_filter={
                                                     'is_teacher': True
                                                 })[0]

    def get_educators_by_name(self,
                              name: str,
                              teaching: list=('all',),
                              active: bool=True) -> QuerySet:
        """
        Get educators by their name.
        :param name: String that starts the educators' name.
        :param teaching: A list of educators' teachings.
        :param active: Filter out inactive educators.
        :return: A QuerySet of educators.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching,
                                                 active=active,
                                                 additional_filter={
                                                     'is_educator': True
                                                 })[0]

    def get_responsibles_by_name(self,
                                 name: str,
                                 teaching: list=('all',),
                                 active: bool=True) -> QuerySet:
        """
        Get responsibles by their name.
        :param name: String that starts the responsibles' name.
        :param teaching: A list of responsibles' teachings.
        :param active: Filter out inactive responsibles.
        :return: A QuerySet of responsibles.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching,
                                                 active=active)[0]

    @staticmethod
    def get_students_by_classe(classe: object, teaching: list=('all',)) -> QuerySet:
        """
        Get students that are in a classe.
        :param classe: A string that describes the classe or a ClasseModel object.
        :param teaching:  A list of teaching that the students belong.
        :return: A QuerySet of students
        """
        if not classe:
            return StudentModel.objects.none()

        students = StudentModel.objects.all().order_by('last_name', 'first_name')
        if "all" not in teaching:
            if type(teaching[0]) == TeachingModel:
                students = students.filter(teaching__in=teaching)
            else:
                students = students.filter(teaching__name__in=teaching)

        if type(classe) == ClasseModel:
            return students.filter(classe=classe)

        # classe is a string.
        if classe[0].isdigit():
            students = students.filter(classe__year=int(classe[0])).order_by('last_name',
                                                                             'first_name')
        else:
            return StudentModel.objects.none()

        if len(classe) > 1:
            return students.filter(classe__letter__istartswith=classe[1:])

        return students


def get_classes(teaching: list = ('all',), check_access: bool = False, user: User = None,
                tenure_class_only: bool = True, educ_by_years: bool = True) -> QuerySet:
    """Get the list of classes.

    :param teaching: A list of students' teachings, defaults to ('all',)
    :type teaching: list, optional
    :param check_access: Return only classes with access, defaults to False
    :type check_access: bool, optional
    :param user: The user trying to get the classes (only usefull with check_access=True), defaults to None
    :type user: User, optional
    :param tenure_class_only: If a teacher, get classes only by tenure, defaults to True
    :type tenure_class_only: bool, optional
    :param educ_by_years: If educator, get classes by year access. Otherwise get it by classes, defaults to True
    :type educ_by_years: bool, optional
    :return: A QuerySet of classes.
    :rtype: QuerySet
    """
    # First, get teaching models.
    if "all" not in teaching:
        if len(teaching) > 0 and type(teaching[0]) == TeachingModel:
            teaching_models = teaching
        else:
            teaching_models = TeachingModel.objects.filter(name__in=teaching)
    else:
        teaching_models = TeachingModel.objects.all()

    if check_access and user:
        try:
            responsible = ResponsibleModel.objects.get(user=user)
            teaching_models = list(teaching_models.intersection(responsible.teaching.all()))
        except ObjectDoesNotExist:
            # Responsible not found return no classes.
            return ClasseModel.objects.none()
        # Sysadmins, direction members, pms have all access.
        if user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP,
                                        settings.PMS_GROUP]).exists():
            return get_classes(teaching_models)

        # Coordonators have by years access.
        if user.groups.filter(name__istartswith=settings.COORD_GROUP).exists():
            years = _get_years_by_group(user)
            return get_classes(teaching_models).filter(year__in=years)

        # Educators have by years or by classes access.
        if user.groups.filter(name__istartswith=settings.EDUC_GROUP).exists():
            if educ_by_years:
                years = _get_years_by_group(user)
                return get_classes(teaching_models).filter(year__in=years)
            else:
                return responsible.classe.all().filter(teaching__in=teaching_models)

        # It should be a teacher.
        if tenure_class_only:
            return responsible.tenure.all().filter(teaching__in=teaching_models)
        else:
            return responsible.classe.all().filter(teaching__in=teaching_models).union(
                responsible.tenure.all().filter(teaching__in=teaching_models)
            )
    else:
        return ClasseModel.objects.filter(teaching__in=teaching_models)


def get_years(
    teaching: list = ("all",),
    check_access: bool = False,
    user: User = None,
    tenure_class_only: bool = True,
    educ_by_years: bool = True
) -> set:
    """
    Get the list of years.
    :param teaching: A list of students' teachings.
    :param check_access: Return only classes with access, defaults to False
    :type check_access: bool, optional
    :param tenure_class_only: If a teacher, get classes only by tenure, defaults to True
    :type tenure_class_only: bool, optional
    :param educ_by_years: If educator, get classes by year access. Otherwise get it by classes,
        defaults to True
    :type educ_by_years: bool, optional
    :return: A set of years.
    """
    classes = get_classes(teaching, check_access, user, tenure_class_only, educ_by_years)
    return set(map(lambda s: s.year, classes))


def _get_years_by_group(user: User) -> set:
    groups = user.groups.values_list("name", flat=True)
    return set(map(lambda g: int(g[-1]), filter(lambda g: g[-1].isdigit(), groups)))


def check_access_to_student(
    student: StudentModel,
    user: User,
    tenure_class_only: bool = True,
    educ_by_years: bool = True
) -> bool:
    """Check if user can see a specific student.

    :param student: The student the user try to access.
    :type student: StudentModel
    :param user: The user who tries to access the student.
    :type user: User
    :param tenure_class_only: If a teacher, get classes only by tenure, defaults to True
    :type tenure_class_only: bool, optional
    :param educ_by_years: If educator, get classes by year access. Otherwise get it by classes,
        defaults to True
    :type educ_by_years: bool, optional
    :return: Wether the user can access or not to the student.
    """

    if not user or user.is_anonymous:
        return False

    privileged_group = get_privileged_group(user)

    # Sysadmins, direction members, pms have all access.
    if privileged_group in [settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.PMS_GROUP]:
        return True

    try:
        responsible = ResponsibleModel.objects.get(user=user)
    except ObjectDoesNotExist:
        return False

    # Coordinators have by years access.
    if privileged_group == settings.COORDONATOR_GROUP:
        if user.groups.filter(name__istartswith=settings.COORD_GROUP).exists():
            return student.classe.year in _get_years_by_group(user)

    # Educators have by years or by classes access.
    if privileged_group == settings.EDUCATOR_GROUP:
        if user.groups.filter(name__istartswith=settings.EDUC_GROUP).exists():
            if educ_by_years:
                return student.classe.year in _get_years_by_group(user)
            else:
                return responsible.classe.filter(id=student.classe.id).exists()

    # Teachers have by tenure or by classes access.
    if privileged_group == settings.TEACHER_GROUP:
        if tenure_class_only:
            return responsible.tenure.filter(id=student.classe.id).exists()
        else:
            teachers = get_teachers_from_student(student)
            return responsible in teachers

    return False


def get_teachers_from_student(stud: StudentModel) -> QuerySet:
    """Get the student's teachers (tenure included).

    :param stud: The student we are looking at.
    :type stud: StudentModel
    :return: A queryset of teachers.
    :rtype: QuerySet
    """

    stud_teach_rel = get_core_settings().student_teacher_relationship

    if stud_teach_rel == CoreSettingsModel.BY_CLASSES:
        return ResponsibleModel.objects.filter(
            Q(classe=stud.classe) | Q(tenure=stud.classe)
        )
    elif stud_teach_rel == CoreSettingsModel.BY_COURSES:
        courses = stud.courses.values_list("id")
        return ResponsibleModel.objects.filter(courses__id__in=courses)
    elif stud_teach_rel == CoreSettingsModel.BY_CLASSES_COURSES:
        courses = stud.courses.values_list("id")
        return ResponsibleModel.objects.filter(
            Q(classe=stud.classe) | Q(courses__id__in=courses) | Q(tenure=stud.classe)
        )

    return ResponsibleModel.objects.none()


def get_students_from_teacher(resp: ResponsibleModel) -> QuerySet:
    """Get the teacher's students (from classes and tenure).

    :param resp: The responsible (must be a teacher).
    :type resp: ResponsibleModel.
    :return: A Queryset of students.
    :rtype: QuerySet
    """

    if not resp.is_teacher:
        return StudentModel.objects.none()

    stud_teach_rel = get_core_settings().student_teacher_relationship

    if stud_teach_rel == CoreSettingsModel.BY_CLASSES:
        classes = resp.classe.values_list("id").union(resp.tenure.values_list("id"))
        return StudentModel.objects.filter(Q(classe__id__in=classes))
    elif stud_teach_rel == CoreSettingsModel.BY_COURSES:
        courses = resp.courses.values_list("id")
        return StudentModel.objects.filter(courses__id__in=courses)
    elif stud_teach_rel == CoreSettingsModel.BY_CLASSES_COURSES:
        classes = resp.classe.values_list("id").union(resp.tenure.values_list("id"))
        courses = resp.courses.values_list("id")
        return StudentModel.objects.filter(
            Q(classe__id__in=classes) | Q(courses__id__in=courses)
        ).distinct()

    return StudentModel.objects.none()


def get_privileged_group(user: User) -> Union[str, None]:
    """Get the highest privileged group for teaching responsibles.

    sysadmin, direction, pms > coordinator > educator > teacher.

    :param user: The user we are looking at.
    :type user: User
    :return: Either the name of the group from settings or None if there is no group
    """
    if not user or user.is_anonymous:
        return None

    ordered_groups = [
        settings.SYSADMIN_GROUP,
        settings.DIRECTION_GROUP,
        settings.PMS_GROUP,
        settings.COORDONATOR_GROUP,
        settings.EDUCATOR_GROUP,
        settings.TEACHER_GROUP,
    ]

    for group in ordered_groups:
        if user.groups.filter(name=group).exists():
            return group
