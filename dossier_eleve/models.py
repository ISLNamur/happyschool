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
    all_access = models.ManyToManyField(Group,
        default=None,
        blank=True,
        help_text="""Permet à un membre du ou des groupes sélectionnés ayant accès qu'à
        certains niveaux, d'avoir accès à tous les niveaux.
        """
    )
    dir_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="dir_allow_visibility_to",
        help_text="""La liste des groupes qui seront affichés pour le choix de la visibilité
        par un membre de la direction. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    dir_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="dir_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        de la direction. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    coord_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="coord_allow_visibility_to",
        help_text="""La liste des groupes qui seront affichés pour le choix de la visibilité
        par un membre des coordonateurs. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    coord_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="coord_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        d'un coordonateur. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    educ_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="educ_allow_visibility_to",
        help_text="""La liste des groupes qui seront affichés pour le choix de la visibilité
        par un membre des éducateurs. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    educ_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="educ_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        d'un éducateur. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    teacher_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="teacher_allow_visibility_to",
        help_text="""La liste des groupes qui seront affichés pour le choix de la visibilité
        par un membre des professeurs. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    teacher_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="teacher_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        d'un professeur. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    pms_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="pms_allow_visibility_to",
        help_text="""La liste des groupes qui seront affichés pour le choix de la visibilité
        par un membre du pms. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    pms_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="pms_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        du pms. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    tenure_allow_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="tenure_allow_visibility_to",
        help_text="""Les groupes selectionnés pourront donner la visibilité aux titulaires.
        Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    tenure_force_visibility_to = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="tenure_force_visibility_to",
        help_text="""Les groupes selectionnés auront forcément la visibilité sur les cas venant
        du titulaire. Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    tenure_allow_visibility_from = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="tenure_allow_visibility_from",
        help_text="""Les groupes selectionnés auront le titulaire comme choix pour la visibilité.
        Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    tenure_force_visibility_from = models.ManyToManyField(
        Group, default=None, blank=True,
        related_name="tenure_force_visibility_from",
        help_text="""Les groupes selectionnés seront forcément visibles par les titulaires.
        Ne concerne que les groupes 'direction', 'coordonateur',
        'educateur', 'professeur' et 'pms'."""
    )
    enable_submit_sanctions = models.BooleanField(default=True)
    use_school_email = models.BooleanField(default=False)
    filter_teacher_entries_by_tenure = models.BooleanField(
        default=False,
        help_text="Déprécié."
    )
    enable_disciplinary_council = models.BooleanField(
        default=True,
        help_text="""Si activé avec la demande de sanction, permet de prévoir de manière facultative
        une date pour statuer de la pertinence d'une demande de sanction."""
    )
    export_retenues_by_classe_default = models.BooleanField(
        default=False,
        help_text="""Lors de l'export des retenues dans les demandes de sanction, la case pour
        trier par classe sera cochée par défaut."""
    )
    export_retenues_by_sanction_default = models.BooleanField(
        default=False,
        help_text="""Lors de l'export des retenues dans les demandes de sanction, la case pour
        trier par sanction sera cochée par défaut."""
    )


class InfoEleve(models.Model):
    info = models.CharField(max_length=200)

    def __str__(self):
        return self.info


class NotifySanctionModel(models.Model):
    PARENTS = 'PA'
    LEGAL_RESPONSIBLE = 'LR'
    SCHOOL_RESPONSIBLE = 'SR'
    RECIPIENTS_CHOICES = [
        (PARENTS, 'Parents'),
        (LEGAL_RESPONSIBLE, 'Responsable légal'),
        (SCHOOL_RESPONSIBLE, 'Responsable à l\'école (éduc/coord)'),
    ]
    recipient = models.CharField(
        max_length=2,
        choices=RECIPIENTS_CHOICES,
        default=LEGAL_RESPONSIBLE,
    )
    frequency = models.PositiveSmallIntegerField(
        default=5,
        help_text="""Fréquence à laquelle la notification sera envoyé. Par exemple, une fréqunce de 5
            enverra une notification tous les multiples de 5 : à la 5ème, 10ème,… sanctions.
            Une fréquence de 1, enverra une notification à chaque nouvelle sanction."""
    )

    def __str__(self):
        recipient = next(x[1] for x in self.RECIPIENTS_CHOICES if x[0] == self.recipient)
        return "Dest. : %s, fréq. : %i" % (recipient, self.frequency)


class SanctionDecisionDisciplinaire(models.Model):
    sanction_decision = models.CharField(max_length=200)
    is_retenue = models.BooleanField(default=False)
    can_ask = models.BooleanField(default=False)
    notify = models.ManyToManyField(
        NotifySanctionModel,
        blank=True,
        help_text="""Permet d'envoyer une notification aux parents/responsable légal ou responsable de l'école
            (éducateurs/coordonateur) à une fréquence particulière (tous les X fois)."""
    )
    letter_comment = models.TextField(
        help_text="Texte qui sera mis en fin de lettre de sanction (balise html pris en charge).",
        default="",
        blank=True
    )

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
    demandeur = models.CharField(max_length=100)
    sanction_decision = models.ForeignKey(SanctionDecisionDisciplinaire, null=True, blank=True, on_delete=models.SET_NULL)
    notified = models.BooleanField(default=False)
    explication_commentaire = models.CharField(max_length=5000)
    attachments = models.ManyToManyField(CasAttachment, blank=True)
    datetime_sanction = models.DateTimeField("date de la sanction", null=True, blank=True)
    time_sanction_end = models.TimeField("Heure de fin de la sanction", null=True, blank=True)
    datetime_conseil = models.DateTimeField("date du conseil disciplinaire", null=True, blank=True)
    sanction_faite = models.NullBooleanField(default=None, null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.CharField(max_length=100, default="")
    visible_by_educ = models.BooleanField(default=True) # Deprecated
    visible_by_tenure = models.BooleanField(default=False)
    visible_by_groups = models.ManyToManyField(Group, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('set_sanction', 'Can set sanction'),
            ('ask_sanction', 'Can ask sanction'),
        )
