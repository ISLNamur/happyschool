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

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Hidden, HTML, Button
from crispy_forms.bootstrap import FormActions

from bootstrap3_datetime.widgets import DateTimePicker
from django.forms import CheckboxSelectMultiple

# from core.StudentManager import StudentManager

# from .models import Email
from core.models import EmailModel


class EmailsChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.display #+ " : " + obj.email


class TraiterAppelForm(forms.Form):
    """
    Formulaire pour traiter un appel
    """

    name = forms.CharField(
        label='Nom, prénom, classe :',
        max_length=300,
        disabled=True,
        required=False,
    )

    matricule = forms.IntegerField(
        label='Matricule :',
        disabled=True,
        required=False,
    )

    objet = forms.ChoiceField(
        label='Objet :',
        choices=(('Rendez-vous', 'Rendez-vous'), ('Retard', 'Retard'),
                 ('Absence', 'Absence'), ('Message', 'Message'),
                 ('Autre', 'Autre')),
        initial='default',
        required=False,
    )

    motif = forms.ChoiceField(
        label='Motif :',
        choices=(('Médical', 'Médical'), ('Familial', 'Familial'),
                 ('Transports', 'Transports'), ('Inconnu', 'Inconnu'),
                 ('Autre', 'Autre'), ('Voir commentaire(s)', 'Voir commentaire(s)')),
        initial='default',
        required=False,
    )

    datetime_appel = forms.DateTimeField(
        label="Appel à",
        widget=DateTimePicker(),
        required=True,
    )

    commentaires = forms.CharField(
        label="Commentaires (modifiable):",
        widget=forms.Textarea(attrs={'rows': 2}),
        max_length=2000,
        required=False,
    )

    emails = EmailsChoiceField(
        label='Traitement par emails',
        widget=CheckboxSelectMultiple(),
        queryset=EmailModel.objects.all().order_by('-display'),
    )

    custom_email = forms.EmailField(
        label='Autre email : ',
        required=False,
    )

    remarques = forms.CharField(
        label="Autres remarques:",
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=1000,
        required=False,
    )

    datetime_traitement = forms.DateTimeField(
        label="Traitement à",
        widget=DateTimePicker(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', -1)
        self.save_or_later = kwargs.pop('saveButton', 'Traiter plus tard')
        super(TraiterAppelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    """<div class="form-group">
                    <label> Nom: </label>
                    <p class ="form-control-static" > {{ appel.name }} 
                    {% if appel.is_student %}{{ eleve.classe|upper }}{% endif %}</p>
                    </div>
                    <div class ="form-group" >
                    <label > Matricule: </label>
                    <p class ="form-control-static" >{% if appel.is_student %}{{ appel.matricule.matricule }}
                    {% else %}—
                    {% endif %}</p>
                    </div>"""
                ),
                css_class='form-inline'
            ),
            Div(
                Field('datetime_appel'),
                Field('objet'),
                Field('motif'),
                css_class='form-inline',
            ),
            Field('commentaires'),
            Field('emails', template="appels/multipleselect.html"),
            Div(
                Field('custom_email'),
                style="display:none",
                id="custom_email",
            ),
            Field('remarques'),
            Field('datetime_traitement'),
            FormActions(
                Submit('traiter', 'Traiter'),
                Submit('plus_tard', self.save_or_later)
            ),
            Hidden('type', 'traiter'),
            Hidden('id', self.id),
        )


class NouvelAppelForm(forms.Form):
    """
    Formulaire d'un nouvel appel
    """
    name = forms.CharField(
        label='Nom, prénom, classe :',
        max_length=300,
        required=True
    )

    matricule = forms.IntegerField(
        label='Matricule :',
        required=True
    )

    objet = forms.ChoiceField(
        label='Objet :',
        choices=(('default', 'Choisissez un objet'), ('Rendez-vous', 'Rendez-vous'), ('Retard', 'Retard'), ('Absence', 'Absence'), ('Message', 'Message'),
                 ('Autre', 'Autre')),
        initial='default',
        required=False,
    )

    motif = forms.ChoiceField(
        label='Motif :',
        choices=(('default', 'Choisissez un motif'), ('Médical', 'Médical'), ('Familial', 'Familial'), ('Transports','Transports'), ('Inconnu', 'Inconnu'),
                 ('Autre', 'Autre'), ('Voir commentaire(s)', 'Voir commentaire(s)')),
        initial='default',
        required=False,
    )

    datetime_motif_start = forms.DateTimeField(
        label='Début du motif',
        widget=DateTimePicker(),
        required=True,
    )

    datetime_motif_end = forms.DateTimeField(
        label='Fin du motif',
        widget=DateTimePicker(),
        required=True,
    )

    datetime_appel = forms.DateTimeField(
        label="Date et heure d'appel",
        widget=DateTimePicker(),
        required=True,
    )

    commentaires = forms.CharField(
        label="Commentaires :",
        widget=forms.Textarea(),
        max_length=2000,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(NouvelAppelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Div(
                Field('name', id="nomForm", autocomplete='off'),
                Field('matricule', id="matriculeForm", autocomplete='off'),
                css_class='form-inline'
            ),
            Field('objet'),
            Field('motif'),
            Div(
                Field('datetime_motif_start', autocomplete='off'),
                Field('datetime_motif_end', autocomplete='off'),
                css_class='form-inline'
            ),
            Field('datetime_appel'),
            Field('commentaires'),
            Hidden('type', 'nouveau'),
            Submit('submit', 'Soumettre')
        )

    # def is_valid(self):
    #     valid = super(NouvelAppelForm, self).is_valid()
    #
    #     if not valid:
    #         return valid
    #
    #     return not StudentManager().get_person(self.cleaned_data['matricule']) is None
