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
from django.forms import model_to_dict

from .ldap import ldap_to_django, get_django_dict_from_ldap, get_ldap_connection


class TeachingModel(models.Model):
    display_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.display_name, self.name)


class ClasseModel(models.Model):
    year = models.IntegerField()
    letter = models.CharField(max_length=2)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year) + self.letter.upper() + " – " + str(self.teaching.display_name)

    @property
    def compact_str(self):
        return str(self.year) + self.letter.upper()


class StudentModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.PositiveIntegerField(unique=True, primary_key=True)
    teaching = models.ForeignKey(TeachingModel, on_delete=models.CASCADE)
    classe = models.ForeignKey(ClasseModel, on_delete=models.SET_NULL,
                               null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL,
                             null=True, blank=True)

    def __str__(self):
        """Return the full name with the last name first."""
        return '%s %s %s' % (self.last_name, self.first_name, self.classe)

    @property
    def fullname(self):
        return '%s %s' % (self.last_name, self.first_name)

    @property
    def fullname_classe(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.classe.compact_str)

    def get_additional_info(self) -> dict:
        """
        Get additional info about a student.
        The information source could be either an ldap server or the django model provided here.
        """
        if settings.USE_LDAP_INFO:
            connection = get_ldap_connection()
            base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
            # Get attributes we are interested in.
            attributes = list(map(lambda k: k[0], ldap_to_django.items()))
            connection.search(base_dn, "(matricule=%s)" % self.matricule, attributes=attributes)
            if len(connection.response) > 0:
                return get_django_dict_from_ldap(connection.response[0])

            raise Exception("Student (%s) not found in the LDAP directory." % self.matricule)

        return model_to_dict(AdditionalStudentInfo.objects.get(student=self),
                             exclude=['student'])


class AdditionalStudentInfo(models.Model):
    student = models.OneToOneField(StudentModel, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    scolar_year = models.CharField(max_length=9)
    previous_classe = models.CharField(max_length=20)
    orientation = models.CharField(max_length=200)

    birth_date = models.DateField("birth date")
    street = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)

    student_phone = models.CharField(max_length=100)
    student_mobile = models.CharField(max_length=100)
    student_email = models.EmailField(null=True, blank=True)

    resp_last_name = models.CharField(max_length=200)
    resp_first_name = models.CharField(max_length=200)
    resp_phone = models.CharField(max_length=100)
    resp_mobile = models.CharField(max_length=100)
    resp_email = models.EmailField(null=True, blank=True)

    father_last_name = models.CharField(max_length=200)
    father_first_name = models.CharField(max_length=200)
    father_job = models.CharField(max_length=500)
    father_phone = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=100)
    father_email = models.EmailField(null=True, blank=True)

    mother_last_name = models.CharField(max_length=200)
    mother_first_name = models.CharField(max_length=200)
    mother_job = models.CharField(max_length=500)
    mother_phone = models.CharField(max_length=100)
    mother_mobile = models.CharField(max_length=100)
    mother_email = models.EmailField(null=True, blank=True)

    doctor = models.CharField(max_length=200)
    doctor_phone = models.CharField(max_length=200)
    mutual = models.CharField(max_length=200)
    mutual_number = models.CharField(max_length=200)
    medical_information = models.CharField(max_length=500)

    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class ResponsibleModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    matricule = models.BigIntegerField(blank=True, null=True, unique=True)
    teaching = models.ManyToManyField(TeachingModel, blank=True)
    email = models.EmailField()
    email_alias = models.EmailField(blank=True, null=True)
    classe = models.ManyToManyField(ClasseModel, default=None, blank=True)
    tenure = models.ManyToManyField(ClasseModel,
                               blank=True,
                               default=None,
                               related_name="tenure_classe")
    is_teacher = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        """Return the full name with the last name first."""
        return "%s %s" % (self.last_name, self.first_name)

    @property
    def fullname(self):
        return '%s %s' % (self.last_name, self.first_name)

    @property
    def username(self) -> str:
        if settings.USE_LDAP_INFO:
            return self._get_ldap_properties()['username']
        else:
            return self.user.username

    @property
    def password(self) -> str:
        if settings.USE_LDAP_INFO:
            return self._get_ldap_properties()['password']
        else:
            return self.user.password

    def _get_ldap_properties(self):
        if settings.USE_LDAP_INFO:
            connection = get_ldap_connection()
            base_dn = settings.AUTH_LDAP_USER_SEARCH.base_dn
            # Get attributes we are interested in.
            attributes = list(map(lambda k: k[0], ldap_to_django.items()))
            connection.search(base_dn, "(id=%s)" % self.matricule, attributes=attributes)
            if len(connection.response) > 0:
                return get_django_dict_from_ldap(connection.response[0])

            raise Exception("Teacher not found in the LDAP directory.")
        else:
            return None


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
        return self.display
