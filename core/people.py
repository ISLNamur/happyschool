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

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q, QuerySet, Model
from django.db.utils import OperationalError, ProgrammingError

from .models import ResponsibleModel, StudentModel, TeachingModel, ClasseModel

# Person type:
STUDENT = 'student'
TEACHER = 'teacher'
EDUCATOR = 'educator'
RESPONSIBLE = 'responsible'
ALL = 'all'


def get_default_teaching():
    try:
        default_teachings = TeachingModel.objects.filter(default=True)
        if len(default_teachings) == 0:
            default_teachings = TeachingModel.objects.all()

        return list(map(lambda t: t.name, default_teachings))
    except (OperationalError, ProgrammingError):
        pass


def get_all_teachings():
    return list(map(lambda t: t[0], TeachingModel.objects.all().values_list("name")))


class People:
    """
    Class that handles people search and access.
    """
    default_teaching = get_default_teaching()

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
                          teaching: list=default_teaching) -> object:
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
                           teaching: list=default_teaching) -> object:
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
                           teaching: list=default_teaching,
                           person_type=ALL) -> list:
        """
        Get people by their name.
        :param name: String that starts the people's name.
        :param teaching: A list of the person's teachings.
        :param person_type: People's type (students, educators,…).
        :return: A list of Queryset.
        """

        if person_type != ALL:
            get_by_name = getattr(self, "get_%ss_by_name" % person_type, None)
            return get_by_name(name=name, teaching=teaching)

        return list(self.get_students_by_name(name=name, teaching=teaching)) +\
            list(self.get_responsibles_by_name(name=name, teaching=teaching))

    @staticmethod
    def _get_people_by_name_by_model(model_name: Model,
                                     name: str,
                                     teaching: list=default_teaching,
                                     additional_filter: dict={}) -> QuerySet:
        """
        Private method where you can get people by their name and specify the
        model object you expect to have.
        :param model_name: People's model.
        :param name: String that starts the teachers' name.
        :param teaching: A list of teachers' teachings.
        :return: A QuerySet of teachers.
        """
        tokens = name.split(" ")
        people = model_name.objects.none()

        if len(tokens) > 1:
            people = model_name.objects.filter(Q(first_name__unaccent__iexact=tokens[0], last_name__unaccent__istartswith=tokens[1])
                                               | Q(first_name__unaccent__istartswith=tokens[1], last_name__unaccent__iexact=tokens[0]))

        if len(people) == 0:
            for name_part in tokens:
                people |= model_name.objects.filter(Q(first_name__unaccent__istartswith=name_part)
                                                   | Q(last_name__unaccent__istartswith=name_part))

        if teaching and 'all' not in teaching:
            people = people.filter(teaching__name__in=teaching)

        len(people)
        if additional_filter:
            people = people.filter(**additional_filter)

        return people

    def get_students_by_name(self, name: str,
                             teaching: list=default_teaching,
                             classes: list=None) -> QuerySet:
        """
        Get students by their name.
        :param name: String that starts the students' name.
        :param teaching: A list of students' teachings.
        :param classes: A ClasseModel queryset.
        :return: A QuerySet of students.
        """
        students = self._get_people_by_name_by_model(StudentModel,
                                                     name=name,
                                                     teaching=teaching)
        if type(classes) == QuerySet:
            years = set(map(lambda c: c.year, classes))
            letters = set(map(lambda c: c.letter.lower(), classes))
            students = students.filter(classe__year__in=years, classe__letter__in=letters)

        return students

    def get_teachers_by_name(self,
                             name: str,
                             teaching: list=default_teaching) -> QuerySet:
        """
        Get teachers by their name.
        :param name: String that starts the teachers' name.
        :param teaching: A list of teachers' teachings.
        :return: A QuerySet of teachers.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching,
                                                 additional_filter={
                                                     'is_teacher': True
                                                 })

    def get_educators_by_name(self,
                              name: str,
                              teaching: list=default_teaching) -> QuerySet:
        """
        Get educators by their name.
        :param name: String that starts the educators' name.
        :param teaching: A list of educators' teachings.
        :return: A QuerySet of educators.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching,
                                                 additional_filter={
                                                     'is_educator': True
                                                 })

    def get_responsibles_by_name(self,
                                 name: str,
                                 teaching: list=default_teaching) -> QuerySet:
        """
        Get responsibles by their name.
        :param name: String that starts the responsibles' name.
        :param teaching: A list of responsibles' teachings.
        :return: A QuerySet of responsibles.
        """
        return self._get_people_by_name_by_model(ResponsibleModel,
                                                 name=name,
                                                 teaching=teaching)

    def get_students_by_classe(self, classe: str, teaching: list=default_teaching) -> QuerySet:
        """
        Get students that are in a classe.
        :param classe: A string that describes the classe.
        :param teaching:  A list of teaching that the students belong.
        :return: A QuerySet of students
        """
        if len(classe) > 0:
            students = StudentModel.objects.all()
            if classe[0].isdigit():
                students = students.filter(classe__year=int(classe[0]))
            if len(classe) > 1:
                students = students.filter(classe__letter=classe[1].lower())

            return students

        return StudentModel.objects.none()


def _get_years_access(user: User) -> list:
    """
    Get a list of years a user can access, like the years educators or teachers can access.
    :param user: The user object.
    :return: A list of integers that represents the years.
    """
    try:
        teaching = ResponsibleModel.objects.get(user=user).teaching.all()
    except ObjectDoesNotExist:
        # User not found.
        # TODO: Make it work for students.
        return []
    # Sysadmins and direction members have all access
    if user.groups.filter(name__in=['sysadmin', 'direction']).exists():
        return list(set(ClasseModel.objects.filter(teaching__in=teaching).values_list('year', flat=True)))

    # Educators and coordonators years.
    if user.groups.filter(name__istartswith='educ').exists()\
            or user.groups.filter(name__istartswith='coord').exists():
        groups_with_year = filter(lambda g: g.name[-1].isdigit(), user.groups.all())
        return list(set(map(lambda g: int(g.name[-1]), groups_with_year)))

    return []


def _get_classes_access(user: User, teaching: list={"default"}) -> QuerySet:
    """
    Get a list of classes a user can access, like the classes a teacher have.
    :param user: The user we want to have the list of classes.
    :return: A list of strings in the form of strings.
    """
    years = _get_years_access(user)
    classes = ClasseModel.objects.none()

    # Sysadmins and direction members, educators or coordonators.
    if user.groups.filter(name__in=['sysadmin', 'direction', 'educateur']).exists() or \
            user.groups.filter(name__istartswith='coord').exists():
        classes |= get_classes(teaching).filter(year__in=years)

    # Teachers, tenure's classe only.
    if user.groups.filter(name__in=['professeur']).exists():
        teacher = ResponsibleModel.objects.get(user=user)
        classes |= teacher.tenure.all()

    return classes


def get_classes(teaching: list={"default"}, check_access: bool=False, user: User=None) -> QuerySet:
    """
    Get the list of classes.
    :param teaching: A list of students' teachings.
    :return: A set of classes.
    """
    if type(teaching) == set:
        teaching = list(teaching)

    if "default" in teaching and not user:
        teaching.remove("default")
        teaching += get_default_teaching()

    if check_access and user:
        try:
            teachings = ResponsibleModel.objects.get(user=user).teaching.all()
            teachings = list(map(lambda t: t.name, teachings))
            return _get_classes_access(teaching=teachings, user=user)
        except ObjectDoesNotExist:
            # The user is not a responsible and thus no access.
            return set()

    if "all" not in teaching:
        return ClasseModel.objects.filter(teaching__name__in=teaching)
    else:
        return ClasseModel.objects.all()


def get_years(teaching: list={"default"}, check_access: bool=False, user: User=None) -> set:
    """
        Get the list of years.
        :param teaching: A list of students' teachings.
        :return: A set of years.
    """
    if type(teaching) == set:
        teaching = list(teaching)

    if "default" in teaching:
        teaching.remove("default")
        teaching += get_default_teaching()

    if "all" not in teaching:
        classes = ClasseModel.objects.filter(teaching__name__in=teaching)
    else:
        classes = ClasseModel.objects.all()

    if check_access:
        classes = ClasseModel.objects.filter(year__in=_get_years_access(user))

    return set(map(lambda s: s.year, classes))
