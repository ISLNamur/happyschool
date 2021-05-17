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

from django.db import models
from django.contrib.auth.models import Group


class AnnuaireSettingsModel(models.Model):
    can_see_responsibles = models.ManyToManyField(Group, default=None, blank=True, related_name="can_see_responsibles")
    can_see_responsibles_sensitive = models.ManyToManyField(
        Group,
        default=None,
        blank=True,
        related_name="can_see_responsibles_data",
        help_text="Permet aux groupes sélectionnés de voir les données sensibles comme le nom d'utilisateur."
    )
    can_see_student_sensitive = models.ManyToManyField(
        Group,
        default=None,
        blank=True,
        related_name="can_see_student_sensitive",
        help_text="""Permet aux groupes sélectionnés de voir les données sensibles de l'étudiant comme son
            adresse, date de naissance, etc."""
    )
    can_see_student_contact = models.ManyToManyField(Group, default=None, blank=True, related_name="can_see_student_contact")
    can_see_student_medical = models.ManyToManyField(Group, default=None, blank=True, related_name="can_see_student_medical")
    show_credentials = models.BooleanField(
        default=True,
        help_text="""Permet d'afficher/cacher les champs utilisateur/mot de passe dans la fiche info
            et ainsi que la liste des mots de passe des élèves par classe"""
    )
    show_schedule = models.BooleanField(
        default=True,
        help_text="Affiche l'horaire des cours."
    )
