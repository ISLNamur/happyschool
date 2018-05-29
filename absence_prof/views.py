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

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.forms import ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.conf import settings

from .models import Absence, MotifAbsence
from .forms import AbsenceForm

from unidecode import unidecode

from core import email

groups_with_access = [settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.EDUCATOR_GROUP,
                      settings.SECRETARY_GROUP,]
for i in range(1,7):
    groups_with_access.append(settings.COORD_GROUP + str(i))


def add(request):
    form = AbsenceForm(request.POST)
    if form.is_valid():
        absence = None
        if request.POST['type'] == 'new':
            absence = Absence()
        elif request.POST['type'] == 'change':
            absence = Absence.objects.get(pk=int(request.POST['abs_id']))

        if request.POST['id_person'] != '-1':
            absence.id_person = int(request.POST['id_person'])

        absence.name = form.cleaned_data['name']
        absence.datetime_absence_start = form.cleaned_data['datetime_absence_start']
        absence.datetime_absence_end = form.cleaned_data['datetime_absence_end']
        absence.motif = MotifAbsence.objects.get(pk=form.cleaned_data['motif']).motif
        absence.comment = form.cleaned_data['comment']

        absence.datetime_encoding = timezone.now()
        absence.user = request.user.username
        absence.save()

        # Send an email to notify new absence and change.
        subject = '[Absence prof] Nouvelle absence'if request.POST['type'] == 'new'\
            else "[Absence prof] Modification de l'absence"
        context = {'absence': absence, 'new': request.POST['type'] == 'new'}
        if not settings.DEBUG:
            email.send_email(to=['educateurs@isln.be'], subject=subject,
                       email_template='absence_prof/email.html', context=context)
        else:
            email.send_email(to=[settings.EMAIL_ADMIN], subject=subject,
                       email_template='absence_prof/email.html', context=context)
    else:
        raise ValidationError('Error while cleaning absence form')


def remove(request):
    a = Absence.objects.get(pk=request.POST['abs_id'])
    a.delete()


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def index(request):
    if request.method == "POST":
        if request.POST['type'] in ['new', 'change']:
            add(request)

        if request.POST['type'] == 'supprimer':
            remove(request)

    filters = [
        {'val': 'name', 'display': 'Nom et prénom'},
        {'val': 'motif', 'display': "Motif"},
        {'val': 'datetime_absence_start', 'display': "Date de début"},
        {'val': 'datetime_absence_end', 'display': "Date de fin"},
        {'val': 'date_ongoing', 'display': "Par mois"},
        {'val': 'comment', 'display': "Commentaire(s)"},
        {'val': 'status', 'display': "Status"},
    ]

    return render(request, 'absence_prof/index.html', context={'filters': filters})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_absences(request):
    # Récuparation des variables GET
    # On enlève les anciens paramètres
    request.GET = request.GET.copy()
    for k in request.GET:
        request.GET[k] = request.GET[k]

    # La page courrante
    page = request.GET.get("page", 1)
    # Le nombre de cas par page
    rows_by_page = request.GET.get("rpp", 20)
    # L'ordre d'affichage
    order = request.GET.get("sortBy", 'datetime_absence_start')
    # Ordre descendant
    desc = request.GET.get("order", "desc")
    # Filtre sur les cas
    filter_column = request.GET.get("filter", "")
    data1 = request.GET.get("data1", "")
    data2 = request.GET.get("data2", "")
    # Show only active ?
    active = request.GET.get("active", "1")

    all_rows = filter_and_order(request, active=="1", filter_column, data1, data2, order_by=order, order_asc=desc=="asc")

    paginator = Paginator(all_rows, rows_by_page)

    rows_page = None
    try:
        rows_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        rows_page = paginator.page(1)

    rows = []
    for r in rows_page:
        dic = model_to_dict(r)
        status = None
        if timezone.now() > r.datetime_absence_start and timezone.now() - relativedelta(days=1) < r.datetime_absence_end:
        # if r.datetime_absence_start < timezone.now()  < r.datetime_absence_end:
            status = 'En cours'
        elif timezone.now() < r.datetime_absence_start:
            status = 'À venir'
        else:
            status = 'Clôturé'

        dic['status'] = status
        rows.append(dic)

    context = {'absences': rows, 'paginator': rows_page}
    return render(request, 'absence_prof/list.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def add_absence(request, abs_id=-1):
    form = None
    context = {}
    if abs_id != -1:
        absence = Absence.objects.get(pk=abs_id)
        init = {'name': absence.name,
                'datetime_absence_start': absence.datetime_absence_start,
                'datetime_absence_end': absence.datetime_absence_end,
                'motif': MotifAbsence.objects.get(motif=absence.motif).pk,
                'comment': absence.comment}
        id_person = absence.id_person
        if id_person:
            context['matricule'] = id_person
        else:
            id_person = '-1'

        form = AbsenceForm(abs_id=absence.pk, initial=init, person_id=id_person)
    else:
        form = AbsenceForm()

    context['form'] = form
    return render(request, 'absence_prof/add.html', context=context)


def filter_and_order(request, only_actives=False, column=None, data1=None, data2=None, order_by=None, order_asc=False,
                     ens='all'):
    rows = Absence.objects.all()

    # First we filter and order at the query level
    # Filtering
    if only_actives:
        rows = rows.filter(datetime_absence_end__gt=timezone.now() - relativedelta(days=1))
    if column and data1 != '':
        if column == 'name':
            rows = rows.filter(name__icontains=data1)
        if column == 'motif':
            rows = rows.filter(motif__icontains=data1)
        if column == 'comment':
            rows = rows.filter(comment__icontains=data1)

        if column == 'status':
            data1 = unidecode(data1.lower())
            if "en cours".startswith(data1):
                rows = rows.filter(datetime_absence_start__lt=timezone.now(),
                                   datetime_absence_end__gt=timezone.now() - relativedelta(days=1))
            elif "a venir".startswith(data1):
                rows = rows.filter(datetime_absence_start__gt=timezone.now())
            elif "cloture".startswith(data1):
                rows = rows.filter(datetime_absence_end__lt=timezone.now() - relativedelta(days=1))

        # Check if entries are valids
        if column.startswith('datetime') and data2 != '':
            date_1 = timezone.datetime.strptime(data1, '%d/%m/%Y') if type(data1) == str else data1
            date_2 = timezone.datetime.strptime(data2, '%d/%m/%Y') if type(data2) == str else data2
            date_1 = timezone.make_aware(date_1) if timezone.is_naive(date_1) else date_1
            date_2 = timezone.make_aware(date_2) if timezone.is_naive(date_2) else date_2

            if column == 'datetime_encoding':
                rows = rows.filter(datetime_encoding__range=[date_1, date_2])
            elif column == 'datetime_absence_start':
                rows = rows.filter(datetime_absence_start__range=[date_1, date_2])
            elif column == 'datetime_absence_end':
                rows = rows.filter(datetime_absence_end__range=[date_1, date_2])
            else:
                raise Exception("Filter: unknown date column name (" + column + ")")

        elif column.startswith('date') and data2 != '':
            date_1 = timezone.datetime.strptime(data1, '%m/%Y') if type(data1) == str else data1
            date_2 = timezone.datetime.strptime(data2, '%m/%Y') if type(data2) == str else data2
            date_1 = timezone.make_aware(date_1) if timezone.is_naive(date_1) else date_1
            date_2 = timezone.make_aware(date_2) if timezone.is_naive(date_2) else date_2

            if column == 'date_ongoing':
                date_2 = date_2 + relativedelta(months=1)
                rows = rows.filter(datetime_absence_start__lt=date_2, datetime_absence_end__gte=date_1)

    # Ordering
    asc = ''
    if order_asc:
        asc = '-'

    if order_by in ['datetime_absence_start', 'datetime_absence_end']:
        rows = rows.order_by(asc + order_by)

    if order_by in ['name']:
        rows = rows.order_by(asc + 'name')

    return list(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_entries(request, column='name', ens='all'):
    filter_str = request.GET.get('query', '')

    rows = filter_and_order(request, column=column, data1=filter_str)

    entries = []
    if column == 'name':
        entries = map(lambda r: r.name, rows)
        entries = list(set(entries))

    elif column == 'motif':
        entries = list(map(lambda r: r.motif.replace("\r\n", " "), rows))

    elif column == 'comment':
        entries = list(map(lambda r: r.comment[:40].replace("\r\n", " "), rows))

    elif column == 'motif_choice':
        motifs = MotifAbsence.objects.filter(motif__icontains=filter_str)
        entries = list(map(lambda m: m.motif, motifs))

    elif column == 'status':
        entries = ['En cours', 'À venir', 'Clôturé']

    else:
        raise Exception('column name is not valid')

    return JsonResponse(entries, safe=False)
