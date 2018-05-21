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

from core.models import StudentModel, TeachingModel


class DossierEleveSettingsModel(models.Model):
    teachings = models.ManyToManyField(TeachingModel, default=None)
    all_access = models.ManyToManyField(Group, default=None, blank=True)
    enable_submit_sanctions = models.BooleanField(default=True)


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
    datetime_encodage = models.DateTimeField("date d'encodage")
    info = models.ForeignKey(InfoEleve, null=True, blank=True, on_delete=models.SET_NULL)
    demandeur = models.CharField(max_length=50)
    sanction_decision = models.ForeignKey(SanctionDecisionDisciplinaire, null=True, blank=True, on_delete=models.SET_NULL)
    explication_commentaire = models.CharField(max_length=2000)
    datetime_sanction = models.DateTimeField("date de la sanction", null=True, blank=True)
    datetime_conseil = models.DateTimeField("date du conseil disciplinaire", null=True, blank=True)
    sanction_faite = models.NullBooleanField(default=None, null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.CharField(max_length=20, default="")
    visible_by_educ = models.BooleanField(default=True)
    visible_by_tenure = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('access_dossier_eleve', 'Can access to dossier_eleve data'),
        )
