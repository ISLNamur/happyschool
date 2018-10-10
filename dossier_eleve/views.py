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
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.db.models import Count, Q
from django.core.exceptions import ObjectDoesNotExist

# Vue app imports
import json

from django_filters import rest_framework as filters

from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.parsers import FileUploadParser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from core.views import BaseFilters, BaseModelViewSet
from core.utilities import get_menu

from .serializers import *
from .models import *
from .tasks import task_send_info_email

from z3c.rml import rml2pdf
from io import BytesIO
from PyPDF2 import PdfFileMerger


from core.utilities import get_scholar_year, check_student_photo
from core.email import send_email
from core.models import StudentModel, EmailModel, ResponsibleModel
from core.people import People, get_classes, get_years


from .models import CasEleve, InfoEleve, SanctionDecisionDisciplinaire, DossierEleveSettingsModel
from .forms import NouveauCasForm, GenerateSummaryPDFForm, GenDisciplinaryCouncilForm, GenRetenueForm


SANCTIONS_RETENUE = [2, 5, 15, 16]
PMS_EMAIL = 8

groups_with_access = [settings.SYSADMIN_GROUP, settings.TEACHER_GROUP, settings.DIRECTION_GROUP, settings.EDUCATOR_GROUP,
                      settings.SECRETARY_GROUP, settings.PMS_GROUP]

def compute_unread_rows(request):
    if 'dossier_eleve_last_time' in request.session:
        last_time = timezone.datetime.fromtimestamp(request.session['dossier_eleve_last_time'])
        rows = filter_and_order(request, column='datetime_encodage', data1=last_time, data2=timezone.now())
        return len(rows)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_pdf_retenues(request, date=None, date2=None):
    if not date2:
        date2 = date

    rows = filter_and_order(request, column="datetime_sanction", retenues=True,
                            data1=date.replace("-", "/"), data2=date2.replace("-", "/"),
                            order_by="classe")

    retenues = []
    for r in rows:
        dic = model_to_dict(r)
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


def filter_and_order(request, only_actives=False, retenues=False, year=None,
                     column=None, data1=None, data2=None,
                     column2=None, data3=None, data4=None,
                     order_by=None, order_asc=False):
    rows = CasEleve.objects.filter(matricule__isnull=False)

    # Filter the rows from the user teaching.
    try:
        teachings = ResponsibleModel.objects.get(user=request.user).teaching.all()
    except ObjectDoesNotExist:
        # Responsible doesn't exist return null result.
        return []
    rows = rows.filter(matricule__teaching__in=teachings)

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
            rows = rows.filter(name__unaccent__icontains=data1)
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
    if not request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP]).exists():
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

        elif request.user.groups.filter(name=settings.TEACHER_GROUP):
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
        rows = rows.order_by(
            asc + 'matricule__' + order_by + '__year',
            asc + 'matricule__' + order_by + '__letter',
            asc + 'matricule__last_name',
        )

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


def get_settings():
    settings_dossier_eleve = DossierEleveSettingsModel.objects.first()
    if not settings_dossier_eleve:
        # Create default settings.
        settings_dossier_eleve = DossierEleveSettingsModel.objects.create().save()

    return settings_dossier_eleve


class BaseDossierEleveView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       TemplateView):
    permission_required = ('dossier_eleve.access_dossier_eleve')
    filters = []

    def get_context_data(self, **kwargs):
        # Get settings.
        settings_dossier_eleve = get_settings()

        # Add to the current context.
        context = super().get_context_data(**kwargs)
        context['settings'] = JSONRenderer().render(DossierEleveSettingsSerializer(settings_dossier_eleve).data).decode()
        context['menu'] = json.dumps(get_menu(self.request.user, "dossier_eleve"))
        context['filters'] = json.dumps(self.filters)
        scholar_year = get_scholar_year()
        context['current_year'] = json.dumps('%i-%i' % (scholar_year, scholar_year + 1))
        coords = []
        for i in range(1, 7):
            coords.append(settings.COORD_GROUP + str(i))
        context['is_coord'] = json.dumps(self.request.user.groups.filter(
            name__in=coords + [settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP]).exists())
        context['is_educ'] = json.dumps(self.request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.EDUCATOR_GROUP]).exists())
        return context


class DossierEleveView(BaseDossierEleveView):
    template_name = "dossier_eleve/dossier_eleve.html"
    filters = [
        {'value': 'name', 'text': 'Nom'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'info__info', 'text': 'Info'},
        {'value': 'sanction_decision__sanction_decision', 'text': 'Sanction/décision'},
        {'value': 'datetime_encodage', 'text': 'Date encodage'},
        {'value': 'activate_important', 'text': 'Important'},
        {'value': 'matricule_id', 'text': 'Matricule'},
        {'value': 'scholar_year', 'text': 'Année scolaire'},
    ]


class CasEleveFilter(BaseFilters):
    classe = filters.CharFilter(method='classe_by')
    activate_important = filters.BooleanFilter(name="important")
    no_sanctions = filters.BooleanFilter(method="no_sanctions_by")
    no_infos = filters.BooleanFilter(method="no_infos_by")

    class Meta:
        fields_to_filter = ('name', 'matricule_id', 'info__info', 'sanction_decision__sanction_decision',
                            'datetime_encodage', 'scholar_year')
        model = CasEleve
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, name, value):
        if not value[0].isdigit():
            return queryset

        all_access = get_settings().all_access.all()
        if not self.request.user.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
            queryset = queryset.filter(matricule__classe__in=classes)

        if len(value) > 0:
            queryset = queryset.filter(matricule__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(matricule__classe__letter=value[1].lower())
        return queryset

    def no_infos_by(self, queryset, name, value):
        if value:
            return queryset.filter(sanction_decision__isnull=False)
        else:
            return queryset

    def no_sanctions_by(self, queryset, name, value):
        if value:
            return queryset.filter(info__isnull=False)
        else:
            return queryset


class CasEleveViewSet(BaseModelViewSet):
    queryset = CasEleve.objects.filter(matricule__isnull=False)

    serializer_class = CasEleveSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = CasEleveFilter
    ordering_fields = ('datetime_encodage', "matricule__last_name")

    def get_group_all_access(self):
        return get_settings().all_access.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        coords = []
        for i in range(1, 7):
            coords.append(settings.COORD_GROUP + str(i))
        is_coord = self.request.user.groups.filter(name__in=coords + [settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP]).exists()
        is_educ = self.request.user.groups.filter(name__in=[settings.SYSADMIN_GROUP, settings.EDUCATOR_GROUP]).exists()
        if is_educ and not is_coord:
            queryset = queryset.filter(visible_by_educ=True)
        elif not is_educ and not is_coord:
            # Must be a tenure.
            queryset = queryset.filter(visible_by_tenure=True)

        if get_settings().enable_submit_sanctions:
            queryset = queryset.filter(Q(info__isnull=False) | ~Q(sanction_faite=False))
        return queryset

    def perform_create(self, serializer):
        send_to_teachers = serializer.validated_data['send_to_teachers']
        # Remove from serializer as model doesn't need it.
        serializer.validated_data.pop('send_to_teachers')

        super().perform_create(serializer)
        if send_to_teachers:
            task_send_info_email.apply_async(
                countdown=1,
                kwargs={'instance_id': serializer.save().id}
            )

    def perform_update(self, serializer):
        super().perform_update(serializer)

        if serializer.validated_data['send_to_teachers']:
            task_send_info_email.apply_async(
                countdown=1,
                kwargs={'instance_id': serializer.save().id}
            )


class AskSanctionsView(BaseDossierEleveView):
    template_name = "dossier_eleve/ask_sanctions.html"
    filters = [
        {'value': 'name', 'text': 'Nom'},
        {'value': 'classe', 'text': 'Classe'},
        {'value': 'sanction_decision__sanction_decision', 'text': 'Sanction/décision'},
        {'value': 'datetime_sanction', 'text': 'Date sanction'},
        {'value': 'datetime_conseil', 'text': 'Date du conseil'},
        {'value': 'datetime_encodage', 'text': 'Date encodage'},
        {'value': 'matricule_id', 'text': 'Matricule'},
        {'value': 'scholar_year', 'text': 'Année scolaire'},
        {'value': 'activate_all_retenues', 'text': 'Toutes les retenues'},
        {'value': 'activate_not_done', 'text': 'Sanctions non faites'},
        {'value': 'activate_waiting', 'text': 'En attentes de validation'},
    ]


class AskSanctionsFilter(BaseFilters):
    classe = filters.CharFilter(method='classe_by')
    activate_all_retenues = filters.CharFilter(method='activate_all_retenues_by')
    activate_not_done = filters.CharFilter(method='activate_not_done_by')
    activate_waiting = filters.CharFilter(method='activate_waiting_by')

    class Meta:
        fields_to_filter = ('name', 'matricule_id', 'sanction_decision__sanction_decision', 'datetime_sanction',
                            'datetime_conseil', 'datetime_encodage', 'sanction_decision__is_retenue')
        model = CasEleve
        fields = BaseFilters.Meta.generate_filters(fields_to_filter)
        filter_overrides = BaseFilters.Meta.filter_overrides

    def classe_by(self, queryset, name, value):
        if not value[0].isdigit():
            return queryset

        all_access = get_settings().all_access.all()
        if not self.request.user.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
            queryset = queryset.filter(matricule__classe__in=classes)

        if len(value) > 0:
            queryset = queryset.filter(matricule__classe__year=value[0])
            if len(value) > 1:
                queryset = queryset.filter(matricule__classe__letter=value[1].lower())
        return queryset

    def activate_all_retenues_by(self, queryset, name, value):
        if value == 'true':
            retenues = CasEleve.objects.filter(
                matricule__isnull=False,
                sanction_decision__is_retenue=True,
                sanction_faite=False,
            )
            return retenues

    def activate_not_done_by(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(datetime_sanction__lt=timezone.now())
        return queryset

    def activate_waiting_by(self, queryset, name, value):
        if value == 'true':
            return queryset.filter(datetime_conseil__isnull=True, datetime_sanction__isnull=True)
        return queryset


class AskSanctionsViewSet(BaseModelViewSet):
    queryset = CasEleve.objects.filter(matricule__isnull=False, sanction_decision__isnull=False, sanction_faite=False)
    serializer_class = CasEleveSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)
    filter_class = AskSanctionsFilter
    ordering_fields = ('datetime_encodage', 'datetime_sanction', 'matricule__classe__year',
                       'matricule__classe__letter', 'matricule__last_name')

    def get_queryset(self):
        sanctions = SanctionDecisionDisciplinaire.objects.filter(can_ask=True)
        queryset = super().get_queryset().filter(sanction_decision__in=sanctions)
        return queryset

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.save(sanction_faite=False)


class InfoViewSet(ReadOnlyModelViewSet):
    queryset = InfoEleve.objects.all()
    serializer_class = InfoEleveSerializer


class SanctionDecisionViewSet(ReadOnlyModelViewSet):
    queryset = SanctionDecisionDisciplinaire.objects.order_by("sanction_decision")
    serializer_class = SanctionDecisionDisciplinaireSerializer

    def get_queryset(self):
        self.queryset = super().get_queryset()
        only_sanctions = self.request.GET.get('only_sanctions', 0) == "1"
        if only_sanctions:
            return self.queryset.filter(can_ask=True)

        return self.queryset


class StatisticAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, matricule, format=None):
        only_sanctions = request.GET.get('only_sanctions', 1) == 1
        stats = self.gen_stats(request.user, matricule, only_sanctions)
        return Response(json.dumps(stats))

    def gen_stats(self, user_from, matricule, only_sanctions=False, all_years=False):
        all_access = get_settings().all_access.all()
        queryset = CasEleve.objects.all()
        if not user_from.groups.intersection(all_access).exists():
            teachings = ResponsibleModel.objects.get(user=user_from).teaching.all()
            classes = get_classes(list(map(lambda t: t.name, teachings)), True, user_from)
            queryset = queryset.filter(matricule__classe__in=classes)

        cas_discip = queryset.filter(info=None, matricule=matricule)\
                             .filter(Q(sanction_faite=True) | Q(sanction_faite__isnull=True))
        cas_info = queryset.filter(sanction_decision=None, matricule=matricule)

        if not all_years:
            print("not all years")
            current_scolar_year = get_scholar_year()
            limit_date = timezone.make_aware(timezone.datetime(current_scolar_year, 8, 15))
            cas_discip = cas_discip.filter(datetime_encodage__gte=limit_date)
            cas_info = cas_info.filter(datetime_encodage__gte=limit_date)

        sanctions = SanctionStatisticsModel.objects.all()

        stats = []
        for s in sanctions:
            stat = {
                'display': s.display,
                'value': len(cas_discip.filter(sanction_decision__in=s.sanctions_decisions.all()))
            }
            stats.append(stat)

        if not only_sanctions:
            stats.append({'display': 'Non disciplinaire', 'value': len(cas_info)})
            stats.append({'display': 'Total disciplinaire', 'value': len(cas_discip)})

        return stats


class UploadFile(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            attachment = CasAttachment.objects.get(pk=pk)
            serializer = CasAttachmentSerializer(attachment)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, format=None):
        file_obj = request.FILES['file']
        attachment = CasAttachment(attachment=file_obj)
        attachment.save()
        serializer = CasAttachmentSerializer(attachment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            attachment = CasAttachment.objects.get(pk=pk)
            attachment.delete()
        except ObjectDoesNotExist:
            pass

        # As we want the object to be removed, if it's not found, it's ok!
        return Response(status=status.HTTP_200_OK)


class CasElevePDFGenAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if request.GET.get('matricule_id'):
            pdf = self.create_pdf(request)
            if not pdf:
                return render(request, 'dossier_eleve/no_student.html')
            pdf_name = str(request.GET['matricule_id']) + '.pdf'

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
            response.write(pdf.read())
            return response

        if request.GET.get('classe'):
            classe_access = get_classes(get_settings().teachings.all(), True, request.user)
            try:
                classe = classe_access.get(id=request.GET['classe'])
            except ObjectDoesNotExist:
                return HttpResponse("Vous n'avez pas les accès nécessaire.", status=401)

            students = People().get_students_by_classe(classe)
            merger = PdfFileMerger()
            added = False
            for s in students:
                request._request.GET = request.GET.copy()
                request._request.GET['matricule_id'] = s.matricule
                pdf = self.create_pdf(request)
                if not pdf:
                    continue

                merger.append(pdf)
                added = True

            if not added:
                return render(request, 'dossier_eleve/no_student.html')

            output_stream = BytesIO()
            merger.write(output_stream)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename; filename="' + classe.compact_str + '"'
            response.write(output_stream.getvalue())
            return response

        return render(request, 'dossier_eleve/no_student.html')

    @staticmethod
    def create_pdf(request):
        if request._request.GET.get('classe'):
            request._request.GET.pop('classe')
        view_set = CasEleveViewSet.as_view({'get': 'list'})
        results = view_set(request._request).data['results']
        if not results:
            return None

        # Use datetime object instead of plain text.
        for r in results:
            r['datetime_encodage'] = timezone.datetime.strptime(r['datetime_encodage'], "%Y-%m-%dT%H:%M:%S.%f%z")
            if r['info']:
                continue
            r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'], "%Y-%m-%dT%H:%M:%S%z")
        student = StudentModel.objects.get(matricule=request.GET['matricule_id'])
        check_student_photo(student)
        #TODO: Should we show current year statistics or all years statistics?
        context = {'statistics': StatisticAPI().gen_stats(request.user, student,
                                                          all_years=False)}
        tenure = ResponsibleModel.objects.filter(tenure=student.classe).first()
        context['tenure'] = tenure.fullname

        context['student'] = student
        context['list'] = results
        context['absolute_path'] = settings.BASE_DIR

        t = get_template('dossier_eleve/discip_pdf.rml')
        rml_str = t.render(context)

        pdf = rml2pdf.parseString(rml_str)
        return pdf


class AskSanctionsPDFGenAPI(APIView):
    permission_classes = (IsAuthenticated,)
    template = ""
    file_name = ""
    field_date = ""

    def get(self, request, format=None):
        view_set = AskSanctionsViewSet.as_view({'get': 'list'})
        results = view_set(request._request).data['results']
        results = self.modify_entries(results)

        date_from = request.GET.get('datetime_%s__gt' % self.field_date)
        date_to = request.GET.get('datetime_%s__lt' % self.field_date)
        context = {'date_from': date_from, 'date_to': date_to,
                   'list': results}
        t = get_template(self.template)
        rml_str = t.render(context)

        pdf = rml2pdf.parseString(rml_str)
        if not pdf:
            return render(request, 'dossier_eleve/no_student.html')
        pdf_name = self.file_name + '_' + date_from + '_' + date_to + '.pdf'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename; filename="' + pdf_name + '"'
        response.write(pdf.read())
        return response

    def modify_entries(self, results):
        return results


class AskSanctionCouncilPDFGenAPI(AskSanctionsPDFGenAPI):
    template = "dossier_eleve/discip_council.rml"
    file_name = "council"
    field_date = "conseil"

    def modify_entries(self, results):
        for r in results:
            r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'],
                                                                "%Y-%m-%dT%H:%M:%S%z")
            r['datetime_conseil'] = timezone.datetime.strptime(r['datetime_conseil'],
                                                               "%Y-%m-%dT%H:%M:%S%z")
        return results


class AskSanctionRetenuesPDFGenAPI(AskSanctionsPDFGenAPI):
    template = "dossier_eleve/discip_retenues.rml"
    file_name = "retenues"
    field_date = "sanction"

    def modify_entries(self, results):
        for r in results:
            r['datetime_sanction'] = timezone.datetime.strptime(r['datetime_sanction'],
                                                                "%Y-%m-%dT%H:%M:%S%z")
        return results
