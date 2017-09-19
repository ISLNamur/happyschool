from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Hidden
from crispy_forms.bootstrap import Alert

from bootstrap3_datetime.widgets import DateTimePicker

from core.people import People


class ArriveForm(forms.Form):
    """
    Formulaire d'arrivé d'un malade
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

    admission = forms.CharField(
        label="Motifs d'admissions :",
        widget=forms.Textarea(),
        max_length=2000,
        required=True
    )

    datetime_arrive = forms.DateTimeField(
        label='Date et heure d\'arrivée',
        widget=DateTimePicker(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ArriveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'col-sm-8'
        self.helper.layout = Layout(
            Div(
                Field('name', id="nomForm", autocomplete='off'),
                Field('matricule', id="matriculeForm", autocomplete='off'),
                css_class='form-inline'
            ),
            Field('admission'),
            Field('datetime_arrive'),
            Hidden('type', 'nouveau'),
            Alert(content="Un email sera envoyé aux différents responsables de l'élève.", css_class="alert-info"),
            Submit('submit', 'Soumettre')
        )

    def is_valid(self):
        valid = super(ArriveForm, self).is_valid()

        if not valid:
            return valid

        return not People().get_student_by_id(self.cleaned_data['matricule']) is None


class SortieForm(forms.Form):
    """
        Formulaire de sortie d'un malade
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

    admission = forms.CharField(
        label="Motifs d'admissions :",
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=2000,
        required=True
    )

    remarques = forms.CharField(
        label="Remarques de sortie :",
        widget=forms.Textarea(),
        max_length=2000,
    )

    datetime_arrive = forms.DateTimeField(
        label='Date et heure d\'arrivée',
        widget=DateTimePicker(),
        required=True,
    )

    datetime_sortie = forms.DateTimeField(
        label='Date et heure de sortie',
        widget=DateTimePicker(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', -1)
        super(SortieForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'col-sm-8'
        self.helper.layout = Layout(
            Div(
                Field('name', id="nomForm", autocomplete='off'),
                Field('matricule', id="matriculeForm", autocomplete='off'),
                css_class='form-inline'
            ),
            Field('admission'),
            Field('remarques'),
            Field('datetime_arrive', autocomplete='off'),
            Field('datetime_sortie', autocomplete='off'),
            Hidden('type', 'sortie'),
            Hidden('id', self.id),
            Submit('submit', 'Soumettre')
        )
