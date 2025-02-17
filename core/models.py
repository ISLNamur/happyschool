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

from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector

from .ldap import get_ldap_connection


class CoreSettingsModel(models.Model):
    BY_CLASSES = "CL"
    BY_COURSES = "CR"
    BY_CLASSES_COURSES = "BO"
    RELATIONSHIP_CHOICES = [
        (BY_CLASSES, "by classes"),
        (BY_COURSES, "by courses"),
        (BY_CLASSES_COURSES, "by courses and by classes"),
    ]
    school_name = models.CharField(max_length=200, help_text="Nom complet de l'école.", default="")
    school_name_short = models.CharField(
        max_length=10, help_text="Nom court de l'école (abréviation, sigle,…).", default=""
    )
    school_street = models.CharField(max_length=200, default="", blank=True)
    school_postal_code = models.CharField(max_length=20, default="", blank=True)
    school_city = models.CharField(max_length=100, default="", blank=True)
    school_phone = models.CharField(max_length=50, default="", blank=True)
    school_fax = models.CharField(max_length=50, default="", blank=True)
    day_scholar_year_start = models.PositiveSmallIntegerField(default=20)
    month_scholar_year_start = models.PositiveSmallIntegerField(default=8)
    student_teacher_relationship = models.CharField(
        max_length=2,
        choices=RELATIONSHIP_CHOICES,
        default=BY_CLASSES,
        help_text="Comment la relation entre les professeurs et les élèves est établie.",
    )
    root = models.URLField(
        "Root URL",
        help_text="URL vers le serveur HappySchool principal",
        blank=True,
        null=True,
        default=None,
    )
    remote = models.URLField(
        "Remote URL",
        help_text="URL vers un serveur HappySchool distant",
        blank=True,
        null=True,
        default=None,
    )
    remote_token = models.CharField(
        max_length=50,
        help_text="Token généré sur le serveur distant",
        blank=True,
        null=True,
        default=None,
    )


class TeachingModel(models.Model):
    display_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100, help_text="Nom simple pour la programmation.")

    def __str__(self):
        return "%s (%s)" % (self.display_name, self.name)


class ClasseModel(models.Model):
    year = models.IntegerField()
    letter = models.CharField(max_length=20)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year) + self.letter.upper() + " – " + str(self.teaching.display_name)

    @property
    def compact_str(self):
        return str(self.year) + self.letter.upper()


class CourseModel(models.Model):
    short_name = models.CharField(max_length=20, blank=True)
    long_name = models.CharField(max_length=240, default="", blank=True)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (%s)" % (self.long_name, self.teaching)


class GivenCourseModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    group = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        name = self.course.long_name if self.course.long_name else self.course.short_name
        return "%s (%s)" % (name, self.group)

    @property
    def classes(self):
        return ", ".join({s.classe.compact_str for s in self.studentmodel_set.distinct("classe")})

    @property
    def teachers(self):
        return [
            {"id": teacher.id, "matricule": teacher.matricule, "fullname": teacher.fullname}
            for teacher in self.responsiblemodel_set.all()
        ]

    @property
    def display(self):
        return self.__str__()


class PeriodCoreModel(models.Model):
    """Model that describes a period of a day.

    Attributes:
        start Starting time of the period.
        end Ending time of the period.
        name Simple alias of the period.
    """

    start = models.TimeField()
    end = models.TimeField()
    name = models.CharField(max_length=200)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)

    @property
    def display(self):
        """Describe the period."""
        return "%s (%s-%s)" % (self.name, str(self.start)[:5], str(self.end)[:5])

    def __str__(self):
        return self.display


class CourseScheduleModel(models.Model):
    course_name = models.CharField(max_length=10, default="")
    period = models.ForeignKey(PeriodCoreModel, on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField()
    place = models.CharField(max_length=100)
    given_course = models.ManyToManyField(GivenCourseModel, blank=True, default=None)
    is_sync = models.BooleanField(default=True)

    @property
    def related_classes(self):
        classes_set = [
            {s.classe.compact_str for s in gc.studentmodel_set.distinct("classe")}
            for gc in self.given_course.all()
        ]
        classes = {cl for sub_list in classes_set for cl in sub_list}
        return ", ".join(classes)

    @property
    def related_responsibles(self):
        responsibles_set = [
            {f"{t.last_name} {t.first_name[0]}." for t in gc.responsiblemodel_set.all()}
            for gc in self.given_course.all()
        ]
        responsibles = {resp for sub_list in responsibles_set for resp in sub_list}
        return ", ".join(responsibles)

    def __str__(self) -> str:
        return f"{self.course_name} le {self.day_of_week} à {self.period}"


class StudentModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.PositiveIntegerField(unique=True, primary_key=True)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    classe = models.ForeignKey(ClasseModel, on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField(GivenCourseModel, default=None, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    inactive_from = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        indexes = [
            GinIndex(
                SearchVector("last_name", "first_name", config="fr_unaccent"),
                name="search_vector_stud_idx",
            )
        ]

    def __str__(self):
        """Return the full name with the last name first."""
        if self.inactive_from:
            return "%s %s (%s)" % (self.last_name, self.first_name, "ancien")
        else:
            return "%s %s %s" % (self.last_name, self.first_name, str(self.classe))

    @property
    def fullname(self):
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def fullname_classe(self):
        return "%s %s %s" % (
            self.last_name,
            self.first_name,
            self.classe.compact_str if self.classe else "Ancien",
        )

    @property
    def display(self):
        return self.__str__()


class AdditionalStudentInfo(models.Model):
    student = models.OneToOneField(StudentModel, primary_key=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True)
    group = models.CharField(max_length=100, blank=True)
    scholar_year = models.CharField(max_length=9, blank=True)
    previous_classe = models.CharField(max_length=20, blank=True)
    orientation = models.CharField(max_length=200, blank=True)

    birth_date = models.DateField("birth date", null=True, blank=True)
    street = models.CharField(max_length=500, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    locality = models.CharField(max_length=200, blank=True)

    student_phone = models.CharField(max_length=100, blank=True)
    student_mobile = models.CharField(max_length=100, blank=True)
    student_email = models.EmailField(null=True, blank=True)

    resp_last_name = models.CharField(max_length=200, blank=True)
    resp_first_name = models.CharField(max_length=200, blank=True)
    resp_phone = models.CharField(max_length=100, blank=True)
    resp_mobile = models.CharField(max_length=100, blank=True)
    resp_email = models.EmailField(null=True, blank=True)

    father_last_name = models.CharField(max_length=200, blank=True)
    father_first_name = models.CharField(max_length=200, blank=True)
    father_job = models.CharField(max_length=500, blank=True)
    father_phone = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=100, blank=True)
    father_email = models.EmailField(null=True, blank=True)

    mother_last_name = models.CharField(max_length=200, blank=True)
    mother_first_name = models.CharField(max_length=200, blank=True)
    mother_job = models.CharField(max_length=500, blank=True)
    mother_phone = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=100, blank=True)
    mother_email = models.EmailField(null=True, blank=True)

    doctor = models.CharField(max_length=200, blank=True)
    doctor_phone = models.CharField(max_length=200, blank=True)
    mutual = models.CharField(max_length=200, blank=True)
    mutual_number = models.CharField(max_length=200, blank=True)
    medical_information = models.CharField(max_length=500, blank=True)

    username = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=200, blank=True)


class ResponsibleModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.BigIntegerField(null=True, unique=True)
    teaching = models.ManyToManyField(TeachingModel, blank=True)
    email = models.EmailField(blank=True, null=True)
    email_school = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True)
    classe = models.ManyToManyField(ClasseModel, default=None, blank=True)
    courses = models.ManyToManyField(GivenCourseModel, default=None, blank=True)
    tenure = models.ManyToManyField(
        ClasseModel, blank=True, default=None, related_name="tenure_classe"
    )
    is_teacher = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    is_sync = models.BooleanField(default=True)
    inactive_from = models.DateTimeField(null=True, blank=True, default=None)
    birth_date = models.DateField("birth date", null=True, blank=True)

    class Meta:
        indexes = [
            GinIndex(
                SearchVector("last_name", "first_name", config="fr_unaccent"),
                name="search_vector_resp_idx",
            )
        ]

    def __str__(self):
        """Return the full name with the last name first."""
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def fullname(self):
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def password(self) -> str:
        if settings.USE_LDAP_INFO:
            password = self._get_ldap_properties()[settings.AUTH_LDAP_USER_ATTR_MAP["password"]]
            if type(password) == list:
                password = password[0]
            return password
        else:
            return self.user.password

    def _get_ldap_properties(self):
        if settings.USE_LDAP_INFO:
            connection = get_ldap_connection()
            base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
            # Assume username is unique.
            ldap_username_attr = settings.AUTH_LDAP_USER_ATTR_MAP["username"]
            connection.search(
                base_dn, "(%s=%s)" % (ldap_username_attr, self.user.username), attributes="*"
            )
            if len(connection.response) > 0:
                return connection.response[0]["attributes"]

            raise Exception("Teacher not found in the LDAP directory.")
        else:
            return None

    @property
    def display(self):
        return self.__str__()


class YearModel(models.Model):
    year = models.IntegerField("year")

    def __str__(self):
        return str(self.year)


class EmailModel(models.Model):
    email = models.EmailField()
    display = models.CharField(max_length=300, default="")
    teaching = models.ForeignKey(TeachingModel, on_delete=models.SET_NULL, null=True, blank=True)
    is_pms = models.BooleanField(default=False)
    years = models.ManyToManyField(YearModel, blank=True)

    def __str__(self):
        return "%s <%s>" % (self.display, self.email)


class ImportCalendarModel(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(help_text="URL du calendrier ics.")

    def __str__(self):
        return self.name


class MenuEntryModel(models.Model):
    display = models.CharField(max_length=20, help_text="Nom qui sera affiché dans le menu.")
    link = models.URLField()
    forced_order = models.PositiveSmallIntegerField(
        null=True, default=None, blank=True, help_text="Forcer une position dans le menu."
    )

    def __str__(self) -> str:
        return f"{self.display} ({self.link})"


class ColumnToFieldImportModel(models.Model):
    MODEL_CHOICES = [
        ("ST", "Student"),
        ("RE", "Responsible"),
    ]

    name = models.CharField(max_length=100)
    model = models.CharField(max_length=2, choices=MODEL_CHOICES)
    column_to_field = models.JSONField()
