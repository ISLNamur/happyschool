# This file is part of Appyschool.
#
# Appyschool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# Appyschool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Appyschool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import model_to_dict
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models import Count
from django.conf import settings

from .models import Passage
from .forms import ArriveForm, SortieForm

from core.people import People, get_classes
from core import email


teachings = ['primaire', 'secondaire']
groups_with_access = ['sysadmin', 'direction', 'educateur', 'secretaire', 'accueil', 'pms']
for i in range(1,7):
    groups_with_access.append("coord" + str(i))


def send_emails(passage, template, subject):
    eleve = People().get_student_by_id(passage.matricule.matricule, teachings)

    image = static("/photos/" + str(passage.matricule.matricule) + ".jpg")
    context = {'eleve': eleve, 'heure_arrive': passage.datetime_arrive, 'commentaire': passage.motifs_admission, 'passage': passage}
    recipients = email.get_resp_emails(eleve)
    recipients_emails = []
    for r in recipients.items():
        recipients_emails.append(r[0])

    if not settings.DEBUG:
        email.send_email(to=recipients, subject="[Infirmerie] %s %s %s" % (subject, eleve.fullname, eleve.classe.compact_str),
                         email_template="infirmerie/" + template + ".html", context=context, images=[image])
    else:
        print("Sending to: " + str(recipients_emails))
        email.send_email(to=[settings.EMAIL_ADMIN], subject="[Infirmerie] %s %s %s" % (subject, eleve.fullname, eleve.classe.compact_str),
                         email_template="infirmerie/" + template + ".html", context=context, images=[image])


def sortie(request):
    form = SortieForm(request.POST)
    if form.is_valid():
        p = Passage.objects.get(pk=request.POST['id'])
        p.motifs_admission = form.cleaned_data['admission']
        p.remarques_sortie = form.cleaned_data['remarques']
        p.datetime_arrive = form.cleaned_data['datetime_arrive']
        p.datetime_sortie = form.cleaned_data['datetime_sortie']
        p.name = p.matricule.last_name + " " + p.matricule.first_name

        # Send emails
        send_emails(p, "sortie_email", "Sortie de")

        p.save()
        return True
    else:
        return False


def nouveau(request):
    form = ArriveForm(request.POST)
    if form.is_valid():
        student = People().get_student_by_id(form.cleaned_data['matricule'], teaching=teachings)
        if not student:
            return False
        p = Passage(matricule=student, datetime_arrive=form.cleaned_data['datetime_arrive'],
                    motifs_admission=form.cleaned_data['admission'], remarques_sortie="",
                    name = student.fullname)

        send_emails(p, "nouveau_email", "Arrivée de")

        p.save()
        return True
    else:
        return False


def supprimer(request):
    p = Passage.objects.get(pk=request.POST['id'])
    p.delete()


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_malades(request):
    # La page courrante
    page = request.GET.get("page", 1)
    # Le nombre de malade par page
    malade_per_page = request.GET.get("rpp", 20)
    # The sorted column
    sort_by = request.GET.get("sortBy", "datetime_arrive")
    # Order
    order = request.GET.get("order", "asc")
    # Enseignement
    ens = request.GET.get("ens", "all")
    # Filtre sur les cas
    filter_column = request.GET.get("filter", "name")
    data1 = request.GET.get("data1", "")
    data2 = request.GET.get("data2", "")
    # Show only active ?
    active = request.GET.get("active", "1")

    passages = filter_and_order(request, active=="1", filter_column, data1, data2, sort_by, order=='asc', ens=ens)

    paginator = Paginator(passages, malade_per_page)

    passage_page = None
    try:
        passage_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        passage_page = paginator.page(1)

    malades = []
    for malade in passage_page:
        student = malade.matricule
        temps_midi = student.teaching == 'secondaire' and int(student.classe[0]) > 4
        dic = model_to_dict(malade)
        dic['firstname'] = student.first_name
        dic['surname'] = student.last_name
        dic['classe'] = student.classe.compact_str
        dic['enseignement'] = student.teaching.display_name
        dic['temps_midi'] = temps_midi

        malades.append(dic)

    context = {'passages': malades, 'paginator': passage_page}
    return render(request, 'infirmerie/list_malades.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def index(request):
    if request.method == "POST":
        if request.POST['type'] == 'sortie':
            sortie(request)
                        
        if request.POST['type'] == 'nouveau':
            nouveau(request)

        if request.POST['type'] == 'supprimer':
            supprimer(request)

    filters = [
        {'val': 'name', 'display': 'Nom et prénom'},
        {'val': 'classe', 'display': 'Classe'},
        {'val': 'datetime_arrive', 'display': "Date d'arrivé"},
        {'val': 'datetime_sortie', 'display': "Date de sortie"},
        {'val': 'motifs_admission', 'display': "Motif(s) d'admission"},
        {'val': 'remarques_sortie', 'display': "Remarque(s) de sortie"},
    ]

    return render(request, 'infirmerie/index.html', context={'filters': filters, 'new_rows': 0})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def ajouter_malade(request):
    context = {'form': ArriveForm()}
    return render(request, 'infirmerie/ajouter_malade.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def encoder_sortie(request, passageId):
    passage = Passage.objects.get(pk=passageId)
    etudiant = passage.matricule

    form = SortieForm(initial={'name': etudiant.last_name + ' ' + etudiant.first_name, 'matricule': etudiant.matricule,
                               'admission': passage.motifs_admission, 'remarques': passage.remarques_sortie,
                               'datetime_arrive': passage.datetime_arrive}
                      , id=passage.pk)

    context = {'matricule': passage.matricule, 'form': form, 'sorti': not passage.datetime_sortie is None,
               'datetime_sortie': passage.datetime_sortie}

    return render(request, 'infirmerie/sortie_malade.html', context=context)


def filter_and_order(request, only_actives=False, column=None, data1=None, data2=None, order_by=None, order_asc=False,
                     ens='all'):
    rows = Passage.objects.filter(matricule__isnull=False)

    # First we filter and order at the query level
    # Filtering
    if only_actives:
        rows = rows.filter(datetime_sortie__isnull=only_actives)
    if ens != 'all':
        rows = rows.filter(matricule__teaching__name=ens)
    if column and data1 != '':
        if column == 'name':
            students = People().get_students_by_name(data1, teaching=[ens])
            rows = rows.filter(matricule__in=students)

        if column == 'matricule':
            rows = rows.filter(matricule__matricule=int(data1))
        if column == 'classe':
            students = People().get_students_by_classe(data1, [ens])
            rows = rows.filter(matricule__in=students)
        if column == 'motif':
            rows = rows.filter(motifs_admission__icontains=data1)
        if column == 'comment':
            rows = rows.filter(remarques_sortie__icontains=data1)

        # Check if entries are valids
        if column.startswith('datetime') and data2 != '':
            date_1 = timezone.datetime.strptime(data1, '%d/%m/%Y') if type(data1) == str else data1
            date_2 = timezone.datetime.strptime(data2, '%d/%m/%Y') if type(data2) == str else data2
            date_1 = timezone.make_aware(date_1) if timezone.is_naive(date_1) else date_1
            date_2 = date_2.replace(hour=23, minute=59)
            date_2 = timezone.make_aware(date_2) if timezone.is_naive(date_2) else date_2

            if column == 'datetime_arrive':
                rows = rows.filter(datetime_arrive__range=[date_1, date_2])
            if column == 'datetime_sortie':
                rows = rows.filter(datetime_sortie__range=[date_1, date_2])

    # Check access
    if not request.user.groups.filter(name__in=['sysadmin', 'direction', 'accueil']).exists():
        auth_classes = get_classes([ens], check_access=True, user=request.user)
        rows = rows.filter(matricule__classe__in=auth_classes)

    # Ordering
    asc = ''
    if order_asc:
        asc = '-'

    if order_by in ['datetime_arrive']:
        rows = rows.order_by(asc + order_by)

    if order_by in ['classe']:
        rows = rows.order_by(asc + 'matricule__' + order_by)

    if order_by in ['name']:
        rows = rows.order_by(asc + 'matricule__last_name')

    if order_by in ['datetime_sortie']:
        rows = rows.annotate(**{'null_' + order_by: Count(order_by)}).order_by('-null_' + order_by,
                                                                                       asc + order_by)

    return list(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_entries(request, column='name', ens='all'):
    filter_str = request.GET.get('query', '')

    malades = filter_and_order(request, column=column, data1=filter_str, ens=ens)

    entries = []
    if column == 'name':
        entries = map(lambda m: m.matricule.last_name + " " + m.matricule.first_name, malades)
        entries = list(set(entries))

    elif column == 'classe':
        entries = map(lambda m: m.matricule.classe.compact_str, malades)
        entries = list(set(entries))

    elif column == 'motifs_admission':
        entries = list(map(lambda m: m.motifs_admission.replace("\r\n", " "), malades))

    elif column == 'remarques_sortie':
        entries = list(map(lambda m: m.remarques_sortie.replace("\r\n", " "), malades))

    return JsonResponse(entries, safe=False)
