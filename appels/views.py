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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms.models import model_to_dict
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count, CharField


from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet


from core import email
from core.people import People, get_classes
from core.models import EmailModel, StudentModel, ResponsibleModel
from core.views import BaseFilters, BaseModelViewSet

from .models import Appel, ObjectModel, MotiveModel
from .serializers import AppelSerializer, ObjectSerializer, MotiveSerializer
from .forms import NouvelAppelForm, TraiterAppelForm


groups_with_access = ['sysadmin', 'direction', 'educateur', 'secretaire', 'accueil']
for i in range(1, 7):
    groups_with_access.append("coord" + str(i))


def nouveau(request):
    form = NouvelAppelForm(request.POST)
    if form.is_valid():
        a = Appel()
        a.objet = form.cleaned_data['objet']
        a.motif = form.cleaned_data['motif']
        a.commentaire = form.cleaned_data['commentaires']
        a.datetime_motif_start = form.cleaned_data['datetime_motif_start']
        a.datetime_motif_end = form.cleaned_data['datetime_motif_end']
        a.datetime_appel = form.cleaned_data['datetime_appel']
        a.traitement = ""
        a.is_traiter = False
        a.user = request.user.username

        # Check if we have a student or someone else.
        matricule = int(form.cleaned_data['matricule'])
        if matricule > 999 and matricule < 10000:
            student = People().get_student_by_id(matricule, ['all'])
            # studentLDAP = StudentLDAP.objects.get(matricule=matricule)
            a.name = student.fullname
            a.matricule = student
        else:
            a.name = form.cleaned_data['name']
            a.is_student = False

        a.save()
        return True
    else:
        print("wrong form")
        return False


def traiter(request):
    # Add informations/modifications.
    is_traiter = 'traiter' in request.POST

    form = TraiterAppelForm(request.POST)
    if form.is_valid():
        a = Appel.objects.get(pk=request.POST['id'])
        a.objet = form.cleaned_data['objet']
        a.motif = form.cleaned_data['motif']
        a.commentaire = form.cleaned_data['commentaires']
        a.datetime_appel = form.cleaned_data['datetime_appel']
        a.traitement = form.cleaned_data['remarques']
        a.custom_email = form.cleaned_data['custom_email']
        if is_traiter:
            a.datetime_traitement = form.cleaned_data['datetime_traitement']
            a.is_traiter = True

        # Add emails
        a.emails.clear()
        for e in form.cleaned_data['emails']:
            a.emails.add(e)

        a.save()

        # Send emails
        if is_traiter:
            context = {'appel': a}
            image = []
            name = a.name
            if a.is_student:
                # etudiant = student_man.get_person(a.matricule.matricule)
                etudiant = People().get_student_by_id(a.matricule.matricule, ['all'])
                name = str(etudiant)
                context['etudiant'] = etudiant
                image = [static("/photos/" + str(a.matricule.matricule) + ".jpg")]

            sent_to = list(filter(lambda e: e != 'robot@isln.be', map(lambda e: e.email, a.emails.all())))
            if a.custom_email:
                sent_to.append(a.custom_email)
            if not settings.DEBUG:
                email.send_email(to=sent_to, subject="[Appel] %s" % name, email_template="appels/email.html", context=context, images=image)
            else:
                print(sent_to)
                email.send_email(to=[settings.EMAIL_ADMIN], subject="[Appel] %s" % name, email_template="appels/email.html",
                                 context=context, images=image)
    else:
        print(form.errors)


def supprimer(request):
    p = Appel.objects.get(pk=request.POST['id'])
    p.delete()


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_appels(request):
    # Current page
    page = request.GET.get("page", 1)
    # Le nombre de malade par page
    appel_per_page = request.GET.get("rpp", 20)
    # The sorted column
    sort_by = request.GET.get("sortBy", "datetime_appel")
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

    appels = filter_and_order(request, active=='1', filter_column, data1, data2, sort_by, order=='asc', ens)

    paginator = Paginator(appels, appel_per_page)

    appels_page = None
    try:
        appels_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        appels_page = paginator.page(1)

    appels_list = []
    for appel in appels_page:
        dic = model_to_dict(appel)
        if appel.is_student:
            student = appel.matricule
            # temps_midi = student.teaching.name == 'secondaire' and int(student.classe.year) > 4
            dic['firstname'] = student.first_name
            dic['surname'] = student.last_name
            dic['classe'] = student.classe.compact_str
            dic['enseignement'] = student.teaching.display_name

        appels_list.append(dic)

    context = {'appels': appels_list, 'paginator': appels_page}
    return render(request, 'appels/list_appels.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def index(request):
    if request.method == 'POST':
        if request.POST['type'] == 'nouveau':
            nouveau(request)
        elif request.POST['type'] == 'traiter':
            traiter(request)
        elif request.POST['type'] == 'supprimer':
            supprimer(request)

    filters = [
        {'val': 'name', 'display': 'Nom et prénom'},
        {'val': 'objet', 'display': "Objet"},
        {'val': 'motif', 'display': "Motif"},
        {'val': 'datetime_motif_start', 'display': "Date de début"},
        {'val': 'datetime_motif_end', 'display': "Date de fin"},
        {'val': 'datetime_appel', 'display': "Date d'appel"},
        {'val': 'commentaire', 'display': "Commentaire(s)"},
        {'val': 'datetime_traitement', 'display': "Date de traitement"},
    ]

    return render(request, 'appels/index.html', context={'filters': filters})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def nouvel_appel(request):
    context = {'form': NouvelAppelForm()}
    return render(request, 'appels/nouvel_appel.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def traiter_appel(request, appelId):
    appel = Appel.objects.get(pk=appelId)

    # Get prechecked emails based on student class
    prechecked = None
    if len(appel.emails.all()) > 0:
        prechecked = []
        for e in appel.emails.all():
            prechecked.append(e.pk)
    elif appel.is_student:
        # Send to relevant coordonateur and educateur
        prechecked = list(map(lambda e: e.pk, EmailModel.objects.filter(years__year=appel.matricule.classe.year,
                                                                        teaching=appel.matricule.teaching)))

    save_or_later = None
    if appel.is_traiter:
        save_or_later = 'Sauver'
    else:
        save_or_later = 'Traiter plus tard'

    form = TraiterAppelForm(
        initial={
            'name': appel.name,
            'motif': appel.motif,
            'objet': appel.objet,
            'datetime_appel': appel.datetime_appel,
            'commentaires': appel.commentaire,
            'remarques': appel.traitement,
            'datetime_traitement': appel.datetime_traitement,
            'emails': prechecked,
            'custom_email': appel.custom_email},
        id=appel.pk,
        saveButton=save_or_later)
    
    context = { 'appel': appel, 'form': form}
    if appel.is_student:
        context['eleve'] = appel.matricule

    return render(request, 'appels/traiter_appel.html', context=context)


def filter_and_order(request, only_actives=False, column=None, data1=None, data2=None, order_by=None, order_asc=False,
                     ens='all'):
    rows = Appel.objects.exclude(matricule__isnull=True, is_student=True)

    # First we filter and order at the query level
    # Filtering
    if only_actives:
        rows = rows.filter(datetime_traitement__isnull=True)
    if ens != 'all':
        rows = rows.filter(matricule__enseignement=ens, is_student=True)
    if column and data1 != '':
        if column == 'name':
            # people = People().get_people_by_name(data1, teaching=[ens])
            rows = rows.filter(name__icontains=data1)
        if column == 'matricule':
            rows = rows.filter(matricule__matricule=int(data1))
        if column == 'classe':
            students = People().get_students_by_classe(data1, [ens])
            rows = rows.filter(matricule__in=students)
        if column == 'objet':
            rows = rows.filter(objet__icontains=data1)
        if column == 'motif':
            rows = rows.filter(motif__icontains=data1)
        if column == 'commentaire':
            rows = rows.filter(commentaire__icontains=data1)
        if column == 'traitement':
            rows = rows.filter(traitement__icontains=data1)
        # if column == 'sanction_faite':
        #     rows = rows.filter(sanction_faite='oui'.startswith(data1.lower()))

        if column.startswith('datetime') and data2 != '':
            date_1 = timezone.datetime.strptime(data1, '%d/%m/%Y') if type(data1) == str else data1
            date_2 = timezone.datetime.strptime(data2, '%d/%m/%Y') if type(data2) == str else data2
            date_2 = date_2.replace(hour=23, minute=59)
            date_1 = timezone.make_aware(date_1) if timezone.is_naive(date_1) else date_1
            date_2 = timezone.make_aware(date_2) if timezone.is_naive(date_2) else date_2

            if column == 'datetime_appel':
                rows = rows.filter(datetime_appel__range=[date_1, date_2])
            if column == 'datetime_motif_start':
                rows = rows.filter(datetime_motif_start__range=[date_1, date_2])
            if column == 'datetime_motif_end':
                rows = rows.filter(datetime_motif_end__range=[date_1, date_2])
            if column == 'datetime_traitement':
                rows = rows.filter(datetime_traitement__range=[date_1, date_2])

    # Check access
    if not request.user.groups.filter(name__in=['sysadmin', 'direction', 'accueil']).exists():
        auth_classes = get_classes([ens], check_access=True, user=request.user)
        rows = rows.filter(matricule__classe__in=auth_classes)

    # Ordering
    asc = ''
    if order_asc:
        asc = '-'

    if order_by in ['datetime_appel', 'datetime_motif_start', 'datetime_motif_end']:
        rows = rows.order_by(asc + order_by)

    if order_by in ['classe']:
        rows = rows.order_by(asc + 'matricule__' + order_by)

    if order_by in ['name']:
        rows = rows.order_by(asc + 'matricule__lastname')

    if order_by in ['datetime_traitement']:
        rows = rows.annotate(**{'null_' + order_by: Count(order_by)}).order_by('-null_' + order_by,
                                                                                       asc + order_by)

    # Transform query into a list and thus make the actual query on the database
    return list(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_entries(request, column='name', ens='all'):
    filter_str = request.GET.get('query', '')

    appels = filter_and_order(request, column=column, data1=filter_str, ens=ens)

    entries = []
    if column == 'name':
        entries = map(lambda a: a.name, appels)
        entries = list(set(entries))

    elif column == 'classe':
        entries = map(lambda a: a.matricule.classe.upper(), appels)
        entries = list(set(entries))

    elif column == 'objet':
        entries = list(set(map(lambda m: m.objet, appels)))

    elif column == 'motif':
        entries = list(set(map(lambda m: m.motif, appels)))

    elif column == 'commentaire':
        entries = list(map(lambda m: m.commentaire.replace("\r\n", " "), appels))

    return JsonResponse(entries, safe=False)


import json

def test_vue(request):
    filters = [{'value':'name', 'text':'Nom'}]

    return render(request, "appels/appels.html", context={'filters': json.dumps(filters)})


class AppelFilter(BaseFilters):
    class Meta:
        fields_to_filter = ('name', 'object', 'motive',
             'datetime_motif_start', 'datetime_motif_end',
             'datetime_appel', 'datetime_traitement',
             'is_traiter',)
        model = Appel
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides


class AppelViewSet(BaseModelViewSet):
    queryset = Appel.objects.all()
    filter_access = True
    all_access = ['sysadmin', 'direction', 'secretariat', 'accueil']
    serializer_class = AppelSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = AppelFilter
    ordering_fields = ('name', 'datetime_appel', 'datetime_traitement', 'is_traiter')
    # Default ordering and distinct object cannot be used together.

    def perform_create(self, serializer):
        # Set full name.
        name = serializer.validated_data['matricule'].fullname
        serializer.save(name=name)


class MotiveViewSet(ReadOnlyModelViewSet):
    queryset = MotiveModel.objects.all()
    serializer_class = MotiveSerializer


class ObjectViewSet(ReadOnlyModelViewSet):
    queryset = ObjectModel.objects.all()
    serializer_class = ObjectSerializer
