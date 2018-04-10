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
from django.db.utils import OperationalError, ProgrammingError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Hidden

from bootstrap3_datetime.widgets import DateTimePicker

from .models import MotifAbsence

motifs = [('default', 'Choisissez le motif')]

# Avoid error when no database has been built
try:
    motifs_obj = MotifAbsence.objects.all()
    for m in motifs_obj:
        motifs.append((m.pk, m.motif))

except (OperationalError, ProgrammingError):
    pass


class AbsenceForm(forms.Form):
    name = forms.CharField(
        label='Nom et prénom :',
        max_length=300,
        required=True
    )

    motif = forms.ChoiceField(
        label='Motifs',
        choices=tuple(motifs),
        required=False,
    )

    datetime_absence_start = forms.DateTimeField(
        label="Date du début de l'absence",
        widget=DateTimePicker(),
        required=False,
    )

    datetime_absence_end = forms.DateTimeField(
        label="Date de la fin de l'absence",
        widget=DateTimePicker(),
        required=False,
    )

    comment = forms.CharField(
        label='Commentaire(s)',
        widget=forms.Textarea(),
        max_length=10000,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.abs_id = kwargs.pop('abs_id', -1)
        self.id_person = kwargs.pop('person_id', -1)
        self.type = 'new'
        if self.abs_id >= 0:
            self.type = 'change'
        super(AbsenceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'col-sm-8'
        self.helper.layout = Layout(
            Field('name', id="nomForm", autocomplete='off'),
            Field('motif', autocomplete='off'),
            Field('datetime_absence_start'),
            Field('datetime_absence_end'),
            Field('comment'),
            Hidden('id_person', self.id_person),
            Hidden('abs_id', self.abs_id),
            Hidden('type', self.type),
            Submit('submit', 'Soumettre')
        )
