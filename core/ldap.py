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

import ldap3
from datetime import date

from django.conf import settings


ldap_to_django = {
    "sn": "last_name",
    "cn": "first_name",
    "matricule": "matricule",
    "uid": "username",
    "userPassword": "password",
    "lastActive": "inactive_from",
    "enseignement": "teaching",
    "classeLettre": "classe_letter",
    "an": "year",
    "classe": "classe",
    "genEmail": "email_school",
    "tenure": "tenure",
    "id": "matricule",
    "genre": "gender",
    "ansco": "scholar_year",
    "previousClasse": "previous_classe",
    "orientation": "orientation",
    "dateNaiss": "birth_date",
    "street": "street",
    "postalCode": "postal_code",
    "l": "locality",
    "telephoneEleve": "student_phone",
    "gsmEleve": "student_mobile",
    "emailEleve": "student_email",
    "snResp": "resp_last_name",
    "cnResp": "resp_first_name",
    "telephonePrincipal": "resp_phone",
    "gsmPrincipal": "resp_mobile",
    "email": "resp_email",
    "snFather": "father_last_name",
    "cnFather": "father_first_name",
    "jobFather": "father_job",
    "telephonePere": "father_phone",
    "gsmPere": "father_mobile",
    "emailPere": "father_email",
    "snMother": "mother_last_name",
    "cnMother": "mother_first_name",
    "jobMother": "mother_job",
    "telephoneMere": "mother_phone",
    "gsmMere": "mother_mobile",
    "emailMere": "mother_email",
    "medecin": "doctor",
    "telephoneMedecin": "doctor_phone",
    "mutuelle": "mutual",
    "numeroMutuelle": "mutual_number",
    "infosMedicales": "medical_information",
}


def get_django_dict_from_ldap(ldap_entry: dict) -> dict:
    """
    Translate LDAP attributes into AdditionalStudentInfo attributes.
    :param ldap_entry: The attribute field from the LDAP search.
    :return: A formed dictionary that mimic AdditionalStudentInfo model.
    """
    ldap_attributes = ldap_entry["attributes"]

    django_dict = {}
    for ldap, django in ldap_to_django.items():
        try:
            if ldap == "dateNaiss":
                date_str = ldap_attributes[ldap][0]
                try:
                    django_dict[django] = date(
                        year=int(date_str[:4]), month=int(date_str[4:6]), day=int(date_str[6:])
                    )
                except ValueError:
                    django_dict[django] = date.today()
            elif ldap == "lastActive":
                date_str = ldap_attributes[ldap][0]
                if len(date_str) < 8:
                    continue
                django_dict[django] = date(
                    year=int(date_str[:4]), month=int(date_str[4:6]), day=int(date_str[6:])
                )
            elif ldap not in (
                "enseignement",
                "classe",
                "tenure",
            ):
                if ldap in ldap_attributes:
                    django_dict[django] = ldap_attributes[ldap][0]
                else:
                    if django in django_dict and django_dict[django]:
                        continue
                    django_dict[django] = ""
            else:
                django_dict[django] = ldap_attributes[ldap]
        except KeyError:
            pass

    if "objectClass" in ldap_attributes:
        if "professeur" in ldap_attributes["objectClass"]:
            django_dict["is_teacher"] = True
            if "resp_email" in django_dict:
                django_dict["email"] = django_dict["resp_email"]
        if "educateur" in ldap_attributes["objectClass"]:
            django_dict["is_educator"] = True

    return django_dict


def get_ldap_connection() -> ldap3.Connection:
    server = ldap3.Server(settings.AUTH_LDAP_SERVER_URI, get_info="GET_ALL_INFO")
    conn = ldap3.Connection(
        server,
        settings.AUTH_LDAP_BIND_DN,
        settings.AUTH_LDAP_BIND_PASSWORD,
        read_only=True,
        auto_bind=True,
    )
    return conn
