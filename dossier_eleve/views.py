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

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

from z3c.rml import rml2pdf
from io import BytesIO
from PyPDF2 import PdfFileMerger


from core.utilities import get_scolar_year
from core.email import send_email
from core.models import StudentModel, EmailModel, ResponsibleModel
from core.people import People, get_classes, get_years

# from auth_libreschool.views import has_auth, get_year_access, get_classes_access
# from auth_libreschool import auth

from .models import CasEleve, InfoEleve, SanctionDecisionDisciplinaire
from .forms import NouveauCasForm, GenerateSummaryPDFForm, GenDisciplinaryCouncilForm, GenRetenueForm


SANCTIONS_RETENUE = [2, 5, 15, 16]
PMS_EMAIL = 8

groups_with_access = ['sysadmin', 'direction', 'educateur', 'secretaire', 'professeur', 'pms']


def compute_unread_rows(request):
    if 'dossier_eleve_last_time' in request.session:
        last_time = timezone.datetime.fromtimestamp(request.session['dossier_eleve_last_time'])
        rows = filter_and_order(request, column='datetime_encodage', data1=last_time, data2=timezone.now())
        return len(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['sysadmin', 'direction', 'educateur']),
                  login_url='no_access')
def change_sanction(request, cas_id=None, is_done=None):
    cas = CasEleve.objects.get(pk=cas_id)
    cas.sanction_faite = is_done == "1"
    cas.save()
    return HttpResponse(status=200)


def nouveau(request):
    form = NouveauCasForm(request.POST)
    if form.is_valid():
        explication_commentaire = demandeur = ""
        info = sanction_decision = datetime_sanction = datetime_conseil = None
        sanction_faite = False
        visible_by_educ = visible_by_tenure = True

        if form.cleaned_data['est_disciplinaire'] == 'non_disciplinaire':
            info = InfoEleve.objects.get(pk=form.cleaned_data['info'])
            explication_commentaire = form.cleaned_data['commentaire_info']
            visible_by_educ = form.cleaned_data['visible_by_educ']
            visible_by_tenure = form.cleaned_data['visible_by_tenure']
        else:
            sanction_decision = SanctionDecisionDisciplinaire.objects.get(pk=form.cleaned_data['sanction_decision'])
            datetime_sanction = form.cleaned_data['datetime_sanction']
            explication_commentaire = form.cleaned_data['explication_sanction']
            sanction_faite = form.cleaned_data['sanction_faite']
            if form.cleaned_data['conseil_discipline']:
                datetime_conseil = form.cleaned_data['datetime_conseil']

        c = None

        if int(request.POST['id']) < 0:
            # Create a new entry.
            matricule = form.cleaned_data['matricule']
            try:
                student = People().get_student_by_id(matricule, ['secondaire'])
            except ObjectDoesNotExist:
                print(ObjectDoesNotExist("Student matricule %s does not exist" % matricule))
                return

            # Check authorizations.
            classes = get_classes(teaching=['secondaire'], check_access=True, user=request.user)
            if student.classe not in classes:
                return

            c = CasEleve(matricule=student, name=student.fullname)
            c.datetime_encodage = timezone.now()
            c.user = request.user.username
        else:
            c = CasEleve.objects.get(pk=request.POST['id'])
            # Check authorizations.
            classes = get_classes(teaching=['secondaire'], check_access=True, user=request.user)
            if c.matricule.classe not in classes:
                return

        c.info = info
        c.demandeur = form.cleaned_data['demandeur']
        c.important = form.cleaned_data['important']
        c.sanction_decision = sanction_decision
        c.explication_commentaire = explication_commentaire
        c.datetime_sanction = datetime_sanction
        c.datetime_conseil = datetime_conseil
        c.sanction_faite = sanction_faite
        c.visible_by_educ = visible_by_educ
        c.visible_by_tenure = visible_by_tenure

        # Check if we need to send info to the related teachers
        if info and form.cleaned_data['send_to_teachers']:
            student = People().get_student_by_id(c.matricule.matricule)
            teachers_obj = ResponsibleModel.objects.filters(classes=student.classe)
            # student = student_man.get_person(c.matricule.matricule)
            # teachers_obj = teacher_man.get_people(filters=['classe=' + student.classe, 'enseignement=secondaire'])

            teachers = []
            for t in teachers_obj:
                if not t.gen_email:
                    send_email(to=[settings.EMAIL_ADMIN],
                               subject='ISLN : À propos de ' + student.fullname + " non envoyé à %s" % t.full_name,
                               email_template="dossier_eleve/email_info.html",
                               context={'student': student, 'info': model_to_dict(c), 'info_type': info}
                               )
                else:
                    teachers.append(t.gen_email)

            # Add coord and educs to email list
            teachers += map(lambda e: e.email, EmailModel.objects.filter(teaching=student.teaching, year=student.classe.year))
            teachers.append(EmailModel.objects.get(display='PMS').email)
            # teachers.append(Email.objects.get(pk=CLASS_TO_EMAILS_COORD[int(student.classe[0]) - 1]).email)
            # teachers.append(Email.objects.get(pk=CLASS_TO_EMAILS_EDUC[int(student.classe[0]) - 1]).email)
            # teachers.append(Email.objects.get(pk=PMS_EMAIL).email)

            if not settings.DEBUG:
                try:
                    send_email(to=teachers,
                               subject='ISLN : À propos de ' + student.fullname,
                               email_template="dossier_eleve/email_info.html",
                               context={'student': student, 'info': model_to_dict(c), 'info_type': info}
                               )
                except Exception as err:
                    send_email(to=teachers,
                               subject='ISLN : À propos de ' + student.fullname,
                               email_template="dossier_eleve/email_info.html",
                               context={'student': student, 'info': model_to_dict(c), 'info_type': info}
                               )
            else:
                send_email(to=[settings.EMAIL_ADMIN],
                           subject='ISLN : À propos de ' + student.fullname,
                           email_template="dossier_eleve/email_info.html",
                           context={'student': student, 'info': model_to_dict(c), 'info_type': info}
                           )
                for t in teachers:
                    print("Sending email to : " + t)

        c.save()
    else:
        print("ERROR !!!!!")
        print(form.errors)


def supprimer(request):
    p = CasEleve.objects.get(pk=request.POST['id'])
    p.delete()


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_cas(request):
    # Récuparation des variables GET
    # On enlève les anciens paramètres
    request.GET = request.GET.copy()
    for k in request.GET:
        request.GET[k] = request.GET[k]

    # La page courrante
    page = request.GET.get("page", 1)
    # Le nombre de cas par page
    cas_par_page = request.GET.get("rpp", 20)
    # L'ordre d'affichage
    sort_by = request.GET.get("sortBy", 'datetime_encodage')
    # Ordre descendant
    asc = request.GET.get("order", "desc") == 'asc'
    # Filtre sur les cas
    filter_cas = request.GET.get("filter", None)
    data1 = request.GET.get("data1", None)
    data2 = request.GET.get("data2", None)
    # Show only active ?
    active = request.GET.get("active", "0")
    # Show retenues from all degrees?
    retenues = request.GET.get("retenues", "0")
    # Show cas by scolaryear.
    year = request.GET.get("year", str(get_scolar_year()))

    cas_discip = filter_and_order(request, only_actives=active == "1", retenues=retenues == "1", year=int(year),
                                  column=filter_cas, data1=data1, data2=data2, order_by=sort_by, order_asc=asc)

    paginator = Paginator(cas_discip, cas_par_page)

    cas_page = None
    try:
        cas_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        cas_page = paginator.page(1)

    cas = []
    for c in cas_page:
        dic = model_to_dict(c)
        dic['fullname'] = c.matricule.fullname
        dic['classe'] = c.matricule.classe.compact_str
        if dic['info']:
            dic['info'] = InfoEleve.objects.get(pk=dic['info']).info
        else:
            dic['sanction_decision'] = SanctionDecisionDisciplinaire.objects.get(
                pk=dic['sanction_decision']).sanction_decision
        cas.append(dic)

    context = {'cas': cas, 'paginator': cas_page, }
    is_teacher = request.user.groups.filter(name__in=['professeur']).exists()
    is_direction = not request.user.groups.filter(name__in=['direction']).exists()
    is_coord = not request.user.groups.filter(name__istartswith=['coord']).exists()
    context['is_only_teacher'] = not (is_coord or is_direction) and is_teacher
    return render(request, 'dossier_eleve/list_cas.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def index(request):
    if request.method == "POST":
        if request.POST['type'] == 'nouveau':
            nouveau(request)

        if request.POST['type'] == 'supprimer':
            supprimer(request)

    compute_unread_rows(request)
    request.session['dossier_eleve_last_time'] = timezone.now().timestamp()

    filters = [
        {'val': 'name', 'display': 'Nom et prénom'},
        {'val': 'classe', 'display': 'Classe'},
        {'val': 'datetime_encodage', 'display': "Date d'encodage"},
        {'val': 'info', 'display': 'Info'},
        {'val': 'demandeur', 'display': 'Demandeur'},
        {'val': 'sanction', 'display': 'Sanction/décision'},
        {'val': 'comment', 'display': 'Explication/Commentaire'},
        {'val': 'datetime_council', 'display': 'Date du conseil de discipline'},
        {'val': 'datetime_sanction', 'display': 'Date de la sanction'},
        {'val': 'sanction_faite', 'display': 'Sanction faite ?'},
    ]

    context = { 'is_pms': request.user.username == 'pms', 'filters': filters}
    return render(request, 'dossier_eleve/index.html', context=context)


@login_required
def gen_pdf(request):
    form_summary = GenerateSummaryPDFForm()
    form_council = GenDisciplinaryCouncilForm()
    form_retenues = GenRetenueForm()
    return render(request, 'dossier_eleve/gen_pdf.html', context={'form_sommaire': form_summary,
                                                                  'form_council': form_council,
                                                                  'form_retenues': form_retenues})


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_pdf_council(request, date_from=None, date_to=None):
    rows = filter_and_order(request, only_actives=True, retenues=False,
                            column='datetime_council', data1=date_from.replace("-", "/"), data2=date_to.replace("-", "/"),
                            order_by='classe')

    discip_council = []
    for r in rows:
        dic = model_to_dict(r)
        # student = student_man.get_person(dic['matricule'])
        student = People().get_student_by_id(dic['matricule'])
        dic['classe'] = student.classe.compact_str
        dic['full_name'] = student.fullname
        dic['sanction_decision'] = SanctionDecisionDisciplinaire.objects.get(pk=dic['sanction_decision'])

        discip_council.append(dic)

    context = {'date_from': date_from, 'date_to': date_to,
               'list': discip_council}
    t = get_template('dossier_eleve/discip_council.rml')
    rml_str = t.render(context)

    pdf = rml2pdf.parseString(rml_str)
    if not pdf:
        return render(request, 'dossier_eleve/no_student.html')
    pdf_name = 'council_' + date_from + '_' + date_to + '.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
    response.write(pdf.read())
    return response

    # return render(request, 'dossier_eleve/no_student.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_pdf_retenues(request, date=None):
    rows = filter_and_order(request, column="datetime_sanction", retenues=True,
                            data1=date.replace("-", "/"), data2=date.replace("-", "/"),
                            order_by="classe")

    retenues = []
    for r in rows:
        dic = model_to_dict(r)
        # student = student_man.get_person(dic['matricule'])
        student = People().get_student_by_id(dic['matricule'])
        dic['classe'] = student.classe.compact_str
        dic['full_name'] = student.fullname
        dic['sanction_decision'] = SanctionDecisionDisciplinaire.objects.get(pk=dic['sanction_decision'])

        retenues.append(dic)

    context = {'date': date, 'list': retenues}
    t = get_template('dossier_eleve/discip_retenues.rml')
    rml_str = t.render(context)

    pdf = rml2pdf.parseString(rml_str)
    if not pdf:
        return render(request, 'dossier_eleve/no_student.html')
    pdf_name = 'retenues_' + date + '.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
    response.write(pdf.read())
    return response


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_pdf(request, all_year=False, matricule=None, classe=None, infos=None, sanctions=None):
    response = None

    # year_access = get_year_access(request)
    classe_access = get_classes(['secondaire'], True, request.user)

    if matricule:
        # student = StudentLDAP.objects.get(matricule=matricule)
        student = People().get_student_by_id(matricule)
        # if not int(student.classe[0]) in year_access:
        if student.classe not in classe_access:
            return HttpResponse("Vous n'avez pas les accès nécessaire.", status=401)

        pdf = create_pdf(student, all_year, infos, sanctions)
        if not pdf:
            return render(request, 'dossier_eleve/no_student.html')
        pdf_name = str(matricule) + '.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
        response.write(pdf.read())
        return response

    if classe:
        # if not int(classe[0]) in year_access:
        classes = classe_access.filter(year=int(classe[0]), letter=classe[1].lower(), teaching__name="secondaire")
        if not classes.exists():
            return HttpResponse("Vous n'avez pas les accès nécessaire.", status=401)

        students = []
        for c in classes:
            students += People().get_students_by_classe(c.compact_str)
        # filters = ['classeLettre=' + classe[1], 'an=' + classe[0]]
        # students = student_man.get_people(enseignement='secondaire', filters=filters)

        merger = PdfFileMerger()
        added = False
        for s in students:
            pdf = create_pdf(s, all_year, infos, sanctions)
            if not pdf:
                continue

            merger.append(pdf)
            added = True

        if not added:
            return render(request, 'dossier_eleve/no_student.html')

        output_stream = BytesIO()
        merger.write(output_stream)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename; filename="' + classe + '"'
        response.write(output_stream.getvalue())
        return response

    return response


def create_pdf(student, all_year, infos, sanctions):
    cas = None
    if int(all_year):
        cas = CasEleve.objects.filter(matricule=student)
    else:
        current_scolar_year = get_scolar_year()
        limit_date = timezone.make_aware(timezone.datetime(current_scolar_year, 8, 15))
        cas = CasEleve.objects.filter(matricule=student,
                                      datetime_encodage__gte=limit_date)
    if not cas:
        return None

    if infos == "0":
        cas = cas.filter(sanction_decision__isnull=False)
    if sanctions == "0":
        cas = cas.filter(info__isnull=False)


    context = gen_stats(student)
    tenure = ResponsibleModel.objects.filter(tenure=student.classe).first()
    # tenure = teacher_man.get_people(filters=['tenure=' + student.classe])[0]
    context['tenure'] = tenure.fullname

    context['student'] = student
    context['list'] = cas
    context['absolute_path'] = settings.BASE_DIR

    t = get_template('dossier_eleve/discip_pdf.rml')
    rml_str = t.render(context)

    pdf = rml2pdf.parseString(rml_str)
    return pdf


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def nouveau_cas(request, cas_id=-1):
    cas_id = int(cas_id)
    form = None
    context = {}
    if cas_id < 0:
        form = NouveauCasForm()
    else:
        cas = CasEleve.objects.get(pk=cas_id)
        init = {'matricule': cas.matricule.matricule,
                'name': cas.matricule.fullname_classe,
                'demandeur': cas.demandeur, 'important': cas.important, }
        context['matricule'] = cas.matricule.matricule
        if cas.info:
            init = {**init, **{'est_disciplinaire': "non_disciplinaire",
                               'info': cas.info.pk, 'commentaire_info': cas.explication_commentaire,
                               'visible_by_educ': cas.visible_by_educ, 'visible_by_tenure': cas.visible_by_tenure,
                               }}
        else:
            conseil_discipline = cas.datetime_conseil is not None
            init = {**init, **{'est_disciplinaire': "disciplinaire",
                               'sanction_decision': cas.sanction_decision.pk,
                               'datetime_sanction': cas.datetime_sanction,
                               'explication_sanction': cas.explication_commentaire,
                               'conseil_discipline': conseil_discipline,
                               'datetime_conseil': cas.datetime_conseil,
                               'sanction_faite': cas.sanction_faite,
                               }
                    }
            stat = gen_stats(cas.matricule)
            context = { **context, **stat}

        form = NouveauCasForm(initial=init, id=cas.pk, is_info=cas.info)

    context['form'] = form
    # context['is_coord'] = auth.is_coord(request) or auth.is_direction(request)
    coords = []
    for i in range(1, 7):
        coords.append("coord" + str(i))
    context['is_coord'] = request.user.groups.filter(name__in=coords + ['direction', 'sysadmin']).exists()
    context['is_educ'] = request.user.groups.filter(name__in=['educateur', 'sysadmin']).exists()

    return render(request, 'dossier_eleve/nouveau_cas.html', context)


def gen_stats(matricule):
    current_scolar_year = get_scolar_year()
    limit_date = timezone.make_aware(timezone.datetime(current_scolar_year, 8, 15))


    cas_discip = CasEleve.objects.filter(info=None, matricule=matricule)
    cas_info = CasEleve.objects.filter(sanction_decision=None, matricule=matricule, datetime_encodage__gte=limit_date)

    temps_midi = len(cas_discip.filter(sanction_decision__id=1))
    retenue = len(cas_discip.filter(sanction_decision__id__in=SANCTIONS_RETENUE))
    convoc = len(cas_discip.filter(sanction_decision__id=9)) + len(cas_discip.filter(sanction_decision__id=10)) + len(
        cas_discip.filter(sanction_decision__id=11)) + len(cas_discip.filter(sanction_decision__id=12))
    exclu = len(cas_discip.filter(sanction_decision__id=6)) + len(cas_discip.filter(sanction_decision__id=7)) + len(
        cas_discip.filter(sanction_decision__id=8))
    renvoi = len(cas_discip.filter(sanction_decision__id=4)) + len(cas_discip.filter(sanction_decision__id=3))
    autre = len(cas_discip.filter(sanction_decision__id=14))

    stats = {
             'non_disciplinaire': len(cas_info),
             'temps_midi': temps_midi,
             'retenue': retenue,
             'convoc': convoc,
             'exclu': exclu,
             'renvoi': renvoi,
             'autre': autre,
             'total': len(cas_discip),
            }

    return stats


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_stats(request, matricule):
    stats = gen_stats(matricule)
    return JsonResponse(stats, safe=False)


def filter_and_order(request, only_actives=False, retenues=False, year=None,
                     column=None, data1=None, data2=None,
                     column2=None, data3=None, data4=None,
                     order_by=None, order_asc=False):
    rows = CasEleve.objects.filter(matricule__isnull=False)

    # First we filter and order at the query level
    # Filtering
    if only_actives:
        rows = rows.filter(datetime_conseil__isnull=False)

    if year:
        date_1 = timezone.datetime.strptime(str(year) + "-08-20", '%Y-%m-%d')
        date_2 = timezone.datetime.strptime(str(year + 1) + "-08-19", '%Y-%m-%d')
        rows = rows.filter(datetime_encodage__range=[date_1, date_2])
    if retenues:
        rows = rows.filter(sanction_decision__pk__in=SANCTIONS_RETENUE)
    if column and data1 != '':
        if column == 'name':
            rows = rows.filter(name__icontains=data1)
        if column == 'matricule':
            rows = rows.filter(matricule__matricule=int(data1))
        if column == 'classe':
            students = People().get_students_by_classe(data1, ['secondaire'])
            rows = rows.filter(matricule__in=students)
        if column == 'info':
            rows = rows.filter(info__info__icontains=data1)
        if column == 'sanction':
            # Filter sanction by id
            sanctions = list(map(lambda s: s.pk,
                                 SanctionDecisionDisciplinaire.objects.filter(sanction_decision__icontains=data1)))
            # Filter Cas by info_id
            rows = rows.filter(sanction_decision__in=sanctions)
        if column == 'demandeur':
            rows = rows.filter(demandeur__icontains=data1)
        if column == 'comment':
            rows = rows.filter(explication_commentaire__icontains=data1)
        if column == 'sanction_faite':
            rows = rows.filter(sanction_faite='oui'.startswith(data1.lower()))

        # Check if entries are valids
        if column.startswith('datetime') and data2 != '':
            date_1 = timezone.datetime.strptime(data1, '%d/%m/%Y') if type(data1) == str else data1
            date_2 = timezone.datetime.strptime(data2, '%d/%m/%Y') if type(data2) == str else data2
            date_1 = timezone.make_aware(date_1) if timezone.is_naive(date_1) else date_1
            date_2 = timezone.make_aware(date_2) if timezone.is_naive(date_2) else date_2
            date_1 = date_1.replace(hour=1)
            date_2 = date_2.replace(hour=23)

            if column == 'datetime_encodage':
                rows = rows.filter(datetime_encodage__range=[date_1, date_2])
            if column == 'datetime_council':
                rows = rows.filter(datetime_conseil__range=[date_1, date_2])
            if column == 'datetime_sanction':
                rows = rows.filter(datetime_sanction__range=[date_1, date_2])

    # Check access
    if not request.user.groups.filter(name__in=['sysadmin', 'direction']).exists():
        auth_classes = get_classes(['secondaire'], check_access=True, user=request.user)

        if request.user.groups.filter(name__istartswith='coord').exists():
            if retenues:
                rows = rows.filter(Q(matricule__classe__in=auth_classes)
                                   | Q(sanction_decision__pk__in=SANCTIONS_RETENUE))
            else:
                rows = rows.filter(matricule__classe__in=auth_classes)

        elif request.user.groups.filter(name='educateur'):
            if retenues:
                rows = rows.filter(Q(matricule__classe__in=auth_classes, visible_by_educ=True)
                                   | Q(sanction_decision__pk__in=SANCTIONS_RETENUE))
            else:
                rows = rows.filter(matricule__classe__in=auth_classes, visible_by_educ=True)

        elif request.user.groups.filter(name='professeur'):
            # teacher = teacher_man.get_people(filters=['uid=' + request.user.username])[0]
            classes = ResponsibleModel.objects.get(user=request.user).tenure.all()
            rows = rows.filter(matricule__classe__in=classes, visible_by_tenure=True)


    # Ordering
    asc = ''
    if order_asc:
        asc = '-'

    if order_by in ['datetime_encodage', 'demandeur']:
        rows = rows.order_by(asc + order_by)

    if order_by in ['classe']:
        rows = rows.order_by(asc + 'matricule__' + order_by)

    if order_by in ['name']:
        rows = rows.order_by(asc + 'matricule__last_name')

    if order_by in ['datetime_sanction', 'datetime_conseil', 'sanction_faite']:
        rows = rows.annotate(**{'null_' + order_by: Count(order_by)}).order_by('-null_' + order_by,
                                                                                       asc + order_by)

    # Transform query into a list and thus make the actual query on the database
    return list(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_entries(request, column='name', ens='all'):
    filter_str = request.GET.get('query', '')

    cas_discip = filter_and_order(request, column=column, data1=filter_str)

    entries = []
    if column == 'name':
        entries = map(lambda cas: cas.matricule.fullname, cas_discip)
        entries = list(set(entries))

    elif column == 'classe':
        entries = map(lambda cas: cas.matricule.classe.compact_str, cas_discip)
        entries = list(set(entries))

    elif column == 'info':
        entries = list(set(map(lambda c: c.info.info, cas_discip)))

    elif column == 'sanction':
        entries = list(set(map(lambda c: c.sanction_decision.sanction_decision, cas_discip)))

    elif column == 'demandeur':
        entries = list(set(map(lambda cas: cas.demandeur, cas_discip)))

    elif column == 'sanction_faite':
        entries = [{'id': 'oui', 'name': 'Oui'}, {'id': 'non', 'name': 'Non'}]

    elif column == 'comment':
        entries = list(map(lambda c: c.explication_commentaire[:40].replace("\r\n", " "), cas_discip))

    return JsonResponse(entries, safe=False)
