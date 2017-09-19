from django import forms
from django.db.utils import OperationalError, ProgrammingError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Fieldset, Hidden, HTML, Button
from crispy_forms.bootstrap import FormActions, InlineRadios

from bootstrap3_datetime.widgets import DateTimePicker

from .models import InfoEleve, SanctionDecisionDisciplinaire


infos = [('default', 'Choisissez l\'info')]
sanct = [('default', 'Choisissez la sanction/décision')]

# Avoid error when no database has been built
try:
    infos_obj = InfoEleve.objects.all()
    for i in infos_obj:
        infos.append((i.pk, i.info))

    sanct_obj = SanctionDecisionDisciplinaire.objects.all()
    for s in sanct_obj:
        sanct.append((s.pk, s.sanction_decision))
except (OperationalError, ProgrammingError):
    pass


class NouveauCasForm(forms.Form):
    """
    Formulaire pour ajouter/modifier un cas disciplinaire
    """

    name = forms.CharField(
        label='Nom et prénom :',
        max_length=300,
        required=True,
    )

    matricule = forms.IntegerField(
        label='Matricule :',
        required=True,
    )

    demandeur = forms.CharField(
        label='Demandeur',
        max_length=50,
        required=True,
    )

    important = forms.BooleanField(
        label='Mettre comme important',
        required=False,
    )

    est_disciplinaire = forms.ChoiceField(
        label='Type d\'info',
        choices=(('non_disciplinaire', 'Non disciplinaire'), ('disciplinaire', 'Disciplinaire')),
        required=True
    )

    info = forms.ChoiceField(
        label='Info',
        choices=tuple(infos),
        # initial='default',
        required=False,
    )

    visible_by_educ = forms.BooleanField(
        label='Visible par les éducateurs',
        required=False,
    )

    visible_by_tenure = forms.BooleanField(
        label='Visible par le titulaire',
        required=False,
    )

    send_to_teachers = forms.BooleanField(
        label='Envoyer l\'info par email aux professeurs de la classe de l\'élève',
        required=False,
    )

    commentaire_info = forms.CharField(
        label="Commentaire relatif à l'info :",
        widget=forms.Textarea(),
        max_length=20000,
        required=False,
    )

    sanction_decision = forms.ChoiceField(
        label='Type de sanction/décision',
        choices=tuple(sanct),
        # initial='default',
        required=False,
    )

    datetime_sanction = forms.DateTimeField(
        label='Date sanction',
        widget=DateTimePicker(),
        required=False,
    )

    explication_sanction = forms.CharField(
        label="Explication de la sanction / décision :",
        widget=forms.Textarea(),
        max_length=20000,
        required=False,
    )

    conseil_discipline = forms.BooleanField(
        label='Conseil de discipline',
        required=False,
    )

    datetime_conseil = forms.DateTimeField(
        label='Date du conseil',
        widget=DateTimePicker(),
        required=False,
    )

    sanction_faite = forms.BooleanField(
        label='La sanction a été faite ?',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id', -1)
        self.is_info = kwargs.pop('is_info', False)
        info_css = 'hidden'
        disciplinary_css = 'hidden'
        if self.id >= 0:
            if self.is_info:
                info_css = ''
            else:
                disciplinary_css = ''

        super(NouveauCasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Div(
                Field('name', id="nomForm", autocomplete='off'),
                Field('matricule', id="matriculeForm", autocomplete='off'),
                css_class='form-inline'
            ),
            Field('demandeur', length=50, autocomplete='off'),
            Field('important'),
            InlineRadios('est_disciplinaire'),
            Div(
                Field('info'),
                Field('commentaire_info'),
                Div(
                    Field('visible_by_educ'),
                    Field('visible_by_tenure'),
                    css_class='form-inline',
                ),
                Field('send_to_teachers'),
                css_class=info_css
            ),
            Div(
                Div(
                    Field('sanction_decision'),
                    Field('datetime_sanction'),
                    Field('sanction_faite'),
                    Field('explication_sanction'),
                    Field('conseil_discipline'),
                    Div(Field('datetime_conseil'), css_class='hidden'),
                    css_class='col-sm-7',
                ),
                Div(
                    HTML("""
                        <h4>Récapitulatif :</h4>
                        <dl class="dl-horizontal">
                            <dt>Temps de midi :</dt>
                            <dd id="stat_temps_midi">{{ temps_midi }}</dd>
                            <dt>Retenue(s) :</dt>
                            <dd id="stat_retenue">{{ retenue }}</dd>
                            <dt>Convocat°(s)</dt>
                            <dd id="stat_convoc">{{ convoc }}</dd>
                            <dt>Exclusion(s) :</dt>
                            <dd id="stat_exclu">{{ exclu }}</dd>
                            <dt>Renvoi(s) :</dt>
                            <dd id="stat_renvoi">{{ renvoi }}</dd>
                            <dt>Autres :</dt>
                            <dd id="stat_autre">{{ autre }}</dd>
                        </dl>
                        """),
                    css_class='col-sm-5',
                ),
                css_class='row ' + disciplinary_css
            ),
            Div(css_class="alert alert-warning",
                css_id="alertBox",
                style="display:none"),
            Hidden('type', 'nouveau'),
            Hidden('id', self.id),
            Submit('submit', 'Soumettre')
        )


class GenerateSummaryPDFForm(forms.Form):
    """
        Generating pdf form.
    """

    name = forms.CharField(
        label='Nom et prénom ou classe:',
        max_length=300,
        required=True,
    )

    infos = forms.BooleanField(
        label='Informations',
        initial=True,
        required = False,
    )

    sanctions = forms.BooleanField(
        label='Sanctions',
        initial=True,
        required=False,
    )

    all_year = forms.BooleanField(
        label='Toutes années scolaires confondues',
        initial=False,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GenerateSummaryPDFForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('name', id="nomForm", autocomplete='off'),
            Field('infos'),
            Field('sanctions'),
            Field('all_year'),
            Button('genpdf', 'Créer PDF'),
        )

class GenDisciplinaryCouncilForm(forms.Form):
    """
        Form that generate disciplinary council pdf
    """

    datetime_from = forms.DateTimeField(
        label='À partir du : ',
        widget=DateTimePicker(),
        required=False,
    )

    datetime_to = forms.DateTimeField(
        label="Jusqu'au : ",
        widget=DateTimePicker(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GenDisciplinaryCouncilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('datetime_from', autocomplete='off'),
            Field('datetime_to', autocomplete='off'),
            Button('genpdf_council', 'Créer PDF'),
        )


class GenRetenueForm(forms.Form):
    """
        Form to generate retenue pdf
    """
    date_retenues = forms.DateTimeField(
        label='Jour de la retenue : ',
        widget=DateTimePicker(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GenRetenueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'col-sm-8'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            Field('date_retenues', autocomplete='off'),
            Button('genpdf_retenues', 'Créer PDF'),
        )
