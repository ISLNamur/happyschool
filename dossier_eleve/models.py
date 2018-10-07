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

import string
import random
from time import strftime

from django.db import models
from django.contrib.auth.models import Group, User

from core.models import StudentModel, TeachingModel


def unique_file_name(instance, filename):
    path = strftime('dossier_eleve/%Y/%m/%d/')
    file = "".join(random.choice(string.ascii_letters) for x in range(0, 4)) + "_" + filename
    return path + file


class DossierEleveSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    dir_allow_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                           related_name="dir_allow_visibility_to")
    dir_force_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                           related_name="dir_force_visibility_to")
    coord_allow_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                             related_name="coord_allow_visibility_to")
    coord_force_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                     related_name="coord_force_visibility_to")
    educ_allow_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                          related_name="educ_allow_visibility_to")
    educ_force_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                       related_name="educ_force_visibility_to")
    teacher_allow_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                      related_name="teacher_allow_visibility_to")
    teacher_force_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                      related_name="teacher_force_visibility_to")
    pms_allow_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                         related_name="pms_allow_visibility_to")
    pms_force_visibility_to = models.ManyToManyField(Group, default=None, blank=True,
                                                         related_name="pms_force_visibility_to")
    enable_submit_sanctions = models.BooleanField(default=True)
    use_school_email = models.BooleanField(default=False)


class InfoEleve(models.Model):
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.info


class SanctionDecisionDisciplinaire(models.Model):
    sanction_decision = models.CharField(max_length=200)
    is_retenue = models.BooleanField(default=False)
    can_ask = models.BooleanField(default=False)

    def __str__(self):
        return self.sanction_decision


class CasAttachment(models.Model):
    attachment = models.FileField(upload_to=unique_file_name)


class SanctionStatisticsModel(models.Model):
    display = models.CharField(max_length=100)
    sanctions_decisions = models.ManyToManyField(SanctionDecisionDisciplinaire, blank=True,
                                                 default=None)

    def __str__(self):
        return self.display


class CasEleve(models.Model):
    matricule = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, to_field='matricule', null=True, blank=True)
    # The name field is there only to have some history.
    name = models.CharField(max_length=100, default="")
    datetime_encodage = models.DateTimeField("date d'encodage", auto_now_add=True)
    datetime_modified = models.DateTimeField("Date de modification", auto_now=True)
    info = models.ForeignKey(InfoEleve, null=True, blank=True, on_delete=models.SET_NULL)
    demandeur = models.CharField(max_length=50)
    sanction_decision = models.ForeignKey(SanctionDecisionDisciplinaire, null=True, blank=True, on_delete=models.SET_NULL)
    explication_commentaire = models.CharField(max_length=5000)
    attachments = models.ManyToManyField(CasAttachment, blank=True)
    datetime_sanction = models.DateTimeField("date de la sanction", null=True, blank=True)
    datetime_conseil = models.DateTimeField("date du conseil disciplinaire", null=True, blank=True)
    sanction_faite = models.NullBooleanField(default=None, null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.CharField(max_length=20, default="")
    visible_by_educ = models.BooleanField(default=True) # Deprecated
    visible_by_tenure = models.BooleanField(default=False) # Deprecated
    visible_by_groups = models.ManyToManyField(Group, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('access_dossier_eleve', 'Can access to dossier_eleve data'),
            ('set_sanction', 'Can set sanction'),
        )
