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
