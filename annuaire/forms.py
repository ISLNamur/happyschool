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


class ChercherEleveForm(forms.Form):
    """
    Formulaire pour chercher un élève
    """
    rechercher = forms.CharField(
        label="Rechercher nom, classe, année, …",
        max_length=300,
        required=False,
    )

    enseignement = forms.ChoiceField(
        label='Enseignement :',
        choices=(('all', 'Tous'), ('primaire', 'Primaire'), ('secondaire', 'Secondaire')),
        initial='all',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ChercherEleveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-6'
        self.helper.layout = Layout(
            Div(
                Field('enseignement'),
                Field('rechercher', id="rechercherInput", autocomplete='off'),
                css_class='form-inline'
            ),
        )
