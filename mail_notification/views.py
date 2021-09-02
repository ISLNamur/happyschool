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

from core.people import get_classes
import os
import json
from django.db.models.query import QuerySet

from unidecode import unidecode

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from django_filters import rest_framework as filters

from annuaire.views import create_classes_list
from core.permissions import IsInGroupPermission
from core.utilities import get_menu
from core.views import LargePageSizePagination
from core.models import ResponsibleModel, TeachingModel, ClasseModel
from mail_answer.models import MailTemplateModel
from mail_answer.models import MailAnswerSettingsModel as AnswersSettings

from mail_notification.models import EmailTag, EmailNotification, EmailAttachment, EmailSender,\
    OtherEmailGroupModel, OtherEmailModel, EmailNotificationSettingsModel
from mail_notification.serializers import EmailNotificationSerializer, EmailAttachmentSerializer, EmailSenderSerializer,\
    OtherEmailSerializer, OtherEmailGroupSerializer
from mail_notification.tasks import task_send_emails_notif

CYCLES = ['Cycle inférieur', 'Cycle supérieur']
DEGREES = ["1er degré", "2ème degré", "3ème degré"]
YEARS = ["1ère année", "2ème année", "3ème année", "4ème année", "5ème année", "6ème année"]

def get_menu_entry(active_app, request):
    if not request.user.has_perm('mail_notification.access_mail_notification'):
        return {}
    return {
            "app": "mail_notification",
            "display": "Email",
            "url": "/mail_notification",
            "active": active_app == "mail_notification"
    }

groups_with_access = [settings.SYSADMIN_GROUP, settings.DIRECTION_GROUP, settings.SECRETARY_GROUP]
for i in range(1,7):
    groups_with_access.append(settings.COORD_GROUP + str(i))


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def index(request):
    context = {'menu': json.dumps(get_menu(request, "mail_notification"))}
    return render(request, 'mail_notification/index.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_list(request):
    emails = EmailNotification.objects.all().order_by("-datetime_created")[:20]
    return render(request, 'mail_notification/list.html',
                  context={'emails': emails,
                           'menu': json.dumps(get_menu(request, "mail_notification"))})


def get_settings():
    settings_email_notif = EmailNotificationSettingsModel.objects.first()
    if not settings_email_notif:
        # Create default settings.
        settings_email_notif = EmailNotificationSettingsModel.objects.create().save()

    return settings_email_notif


class HasPermissions(IsInGroupPermission):
    group = groups_with_access


class SendersList(APIView):
    permission_classes = (IsAuthenticated, HasPermissions)

    def get(self, request, teaching, format=None):
        senders = EmailSender.objects.filter(teaching=teaching, groups__in=request.user.groups.all())\
            .distinct()\
            .order_by('sender_email_name')
        serializer = EmailSenderSerializer(senders, many=True)
        return Response(serializer.data)


class EmailsList(APIView):
    permission_classes = (IsAuthenticated, HasPermissions)

    def get(self, request, format=None):
        emails = EmailNotification.objects.all().order_by("-datetime_created")
        serializer = EmailNotificationSerializer(emails, many=True)
        return Response(serializer.data)


class EmailNotificationViewSet(ReadOnlyModelViewSet):
    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions,)

    def get_queryset(self):
        try:
            responsible = ResponsibleModel.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return EmailNotification.objects.none()

        raw_notif = EmailNotification.objects.filter(
            to_type="teachers",
            teaching__in=responsible.teaching.values_list("name", flat=True)
        ).order_by("-datetime_created")[:50]
        filtered_notif = [
            notif.id for notif in raw_notif if self.is_responsible_in_recipients(responsible, notif.email_to)
        ]

        return EmailNotification.objects.filter(id__in=filtered_notif).order_by("-datetime_created")

    def is_responsible_in_recipients(self, responsible: ResponsibleModel, email_to: str) -> QuerySet:
        recipients = email_to.split(',')
        for recipient in recipients:
            # Check if it is the staff.
            if recipient == 'Personnels':
                if not responsible.is_teacher and not responsible.is_educator and not responsible.is_secretary:
                    return True
                else:
                    continue

            # Check if it is a custom group.
            if OtherEmailGroupModel.objects.filter(name=recipient).exists():
                continue

            # So it is directly related to classes.
            years = []
            # If it starts with a digit, it could be a class, a year or a degree.
            if recipient[0].isdigit():
                # Class length is only two.
                if len(recipient) == 2:
                    classes = ClasseModel.objects.filter(
                        year=int(recipient[0]),
                        letter=recipient[1].lower(),
                        teaching__in=responsible.teaching.all()
                    )
                    years.append(int(recipient[0]))
                elif 'année' in recipient:
                    classes = ClasseModel.objects.filter(
                        year=int(recipient[0]),
                        teaching__id__in=responsible.teaching.all().values_list("id", flat=True)
                    )
                    years.append(int(recipient[0]))
                else:
                    # It is a degrée.
                    classes = ClasseModel.objects.filter(
                        year__in=[int(recipient[0]) * 2, int(recipient[0]) * 2 - 1],
                        teaching__id__in=responsible.teaching.all().values_list("id", flat=True)
                    )
                    degree = int(recipient[0])
                    years += [degree * 2, degree * 2 - 1]
            else:
                # It is a cycle.
                if "supérieur" in recipient:
                    years += [4, 5, 6]
                elif "inférieur" in recipient:
                    years += [1, 2, 3]
                elif "Toutes les classes" in recipient:
                    years += [1, 2, 3, 4, 5, 6]
                # elif "Tout le personnel" in recip:
                #
                else:
                    years = []
                classes = ClasseModel.objects.filter(year__in=years, teaching__in=responsible.teaching.all())

            if get_classes(check_access=True, user=responsible.user, tenure_class_only=False).intersection(classes).exists():
                return True
            else:
                continue
        return False


class UploadFile(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated, HasPermissions)

    def put(self, request, format=None):
        file_obj = request.FILES['file']
        attachment = EmailAttachment(attachment=file_obj)
        attachment.save()
        serializer = EmailAttachmentSerializer(attachment)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        try:
            attachment = EmailAttachment.objects.get(pk=pk)
            attachment.delete()
        except ObjectDoesNotExist:
            pass

        # As we want the object to be removed, if it's not found, it's ok!
        return Response(status=status.HTTP_200_OK)


class SendEmailsView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, HasPermissions)

    def post(self, request, *args, **kw):
        email_to_sent = EmailNotification()
        email_to_sent.email_from = request.data.get('email_from')
        email_to_sent.to_type = request.data.get('to_type')
        email_to_sent.email_to = request.data.get('email_to')  # Come as  ['group1,group2,group3'].
        email_to_sent.subject = request.data.get('subject')
        email_to_sent.body = request.data.get('email_content')
        email_to_sent.teaching = request.data.get('teaching')
        try:
            template = MailTemplateModel.objects.get(id=request.data.get('template', -1))
            email_to_sent.answers = template
        except ObjectDoesNotExist:
            pass
        email_to_sent.datetime_created = timezone.now()
        email_to_sent.save()

        tags = request.data.get('tags', None)  # Come as  ['tag1,tag2,tag3'].
        if tags:
            tags = EmailTag.objects.filter(name__in=tags[0].split(','))
            email_to_sent.tags = tags

        attachments = request.data.get('attachments', '').split(',')

        if attachments[0]:
            for a in attachments:
                email_attach = EmailAttachment.objects.get(pk=int(a))
                email_to_sent.attachments.add(email_attach)
                email_to_sent.save()

        email_to_sent.errors = "Prepared."


        send_type = request.data.get('send_type')
        responsibles = request.data.get('responsibles', 'true') == 'true'

        # Render body message.
        template = get_template("mail_notification/email.html")

        context = {
            'body': email_to_sent.body,
            'to_teachers': email_to_sent.to_type == 'teachers',
        }
        if email_to_sent.attachments.all():
            html_files = "<ul>"
            file_names_urls = map(lambda a: (os.path.basename(a.attachment.path)[9:], a.attachment.url.replace("local.isln.be", "app.isln.be")), email_to_sent.attachments.all())
            for name, url in file_names_urls: html_files += '<li><a href="%s">%s</a></li>\n' % (url, name)
            html_files += "</ul>"
            context['files'] = html_files

        # Add a link to a form if asked.
        if email_to_sent.answers:
            url = "https://local.isln.be/mail_answer/answer/specific_uuid/"
            answers_settings = AnswersSettings.objects.first()
            if answers_settings and answers_settings.use_remote:
                url = url.replace("local.isln.be", "app.isln.be")
            context['link_to_form'] = url

        email_to_sent.body = template.render(context)
        email_to_sent.save()

        task = task_send_emails_notif.apply_async(
            countdown=5,
            kwargs={
            'pk': email_to_sent.pk,
            'responsibles': responsibles,
        })
        return Response(status=status.HTTP_201_CREATED)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_email_to_options(request, teaching, to_type):
    query = unidecode(request.GET.get("query", "")).lower()
    if not query:
        return JsonResponse([], safe=False)

    recipients = []
    if not query[0].isdigit():
        recipients += CYCLES
        # Add static groups.
        recipients.append('Toutes les classes')
        if to_type == 'teachers':
            recipients.append('Personnels')
            # Add custom groups
            recipients += list(map(lambda g: g['name'], OtherEmailGroupModel.objects.all().values('name')))
        recipients = list(filter(lambda r: unidecode(r).lower().startswith(query), recipients))
        return JsonResponse(recipients, safe=False)

    recipients += DEGREES + YEARS
    recipients = list(filter(lambda r: unidecode(r).lower().startswith(query), recipients))

    if len(query) == 1:
        recipients += map(lambda c: c.split(" ")[0], sorted(create_classes_list(request, check_access=False, enseignement=teaching,
                                                                  annees=query[0])))
    else:
        recipients += map(lambda c: c.split(" ")[0], sorted(create_classes_list(request, check_access=False, enseignement=teaching,
                                                                  annees=query[0], letters=query[1])))

    return JsonResponse(recipients, safe=False)


@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=groups_with_access), login_url='no_access')
def get_tags_options(request):
    query = unidecode(request.GET.get("query", ""))
    if not query:
        return JsonResponse(list(map(lambda t: t.name, EmailTag.objects.all())), safe=False)

    return JsonResponse(list(map(lambda t: t.name, EmailTag.objects.filter(name__istartswith=query))), safe=False)


class OtherEmailViewSet(ModelViewSet):
    queryset = OtherEmailModel.objects.all()
    serializer_class = OtherEmailSerializer
    permission_classes = (IsAuthenticated, HasPermissions)
    pagination_class = LargePageSizePagination


class OtherEmailGroupViewSet(ModelViewSet):
    queryset = OtherEmailGroupModel.objects.all()
    serializer_class = OtherEmailGroupSerializer
    permission_classes = (IsAuthenticated, HasPermissions)
    pagination_class = LargePageSizePagination
