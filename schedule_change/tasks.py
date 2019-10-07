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

from z3c.rml import rml2pdf

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.template.loader import get_template
from django.db.models import Q, QuerySet
from django.core.files.storage import default_storage

from core.models import ClasseModel, ResponsibleModel, TeachingModel
from core.email import send_email

from .views import get_core_settings
from .models import ScheduleChangeSettingsModel, ScheduleChangeModel, ScheduleChangeCategoryModel


@shared_task(bind=True)
def task_export(self, ids, date_from, date_to, send_to_teachers=False, message=""):
    changes = [ScheduleChangeModel.objects.get(id=c) for c in ids]
    categories = ScheduleChangeCategoryModel.objects.all()
    context = {'date_from': date_from, 'date_to': date_to,
               'list': changes, 'phone': get_settings().responsible_phone,
               'responsible': get_settings().responsible_name,
               'categories': categories}
    t = get_template('schedule_change/summary.rml')
    rml_str = t.render(context)

    pdf_file = rml2pdf.parseString(rml_str)
    pdf_name = 'changement_horaire_' + date_from + '_' + date_to + '.pdf'

    if send_to_teachers:
        classes = ClasseModel.objects.none()
        for c in changes:
            if c.classes:
                classes |= get_classes_from_display(c.classes)

        teachers_involved = ResponsibleModel.objects.filter(
            Q(classe__in=classes) | Q(tenure__in=classes))
        attachments = [{'filename': pdf_name, 'file': pdf_file.read()}]
        settings = get_settings()
        core_settings = get_core_settings()
        teachers_email = [t.email_school for t in teachers_involved] if settings.email_school else \
            [t.email for t in teachers_involved]
        substitutes = []
        for c in changes:
            subs = c.teachers_substitute.filter(is_teacher=True)
            if not subs:
                continue
            substitutes += [t.email_school for t in subs] if settings.email_school \
                else [t.email for t in subs]

        teachers_email += substitutes

        url = core_settings.remote if settings.copy_to_remote else core_settings.root
        context = {'date_from': date_from, 'date_to': date_to,
                   'url': url, 'message': message}
        send_email(set(teachers_email), 'Changement horaire', 'schedule_change/email_summary.html',
                   context=context, attachments=attachments, use_bcc=True)

    # Save file to media.
    saved_file = default_storage.save(pdf_name, pdf_file)
    # Send file url to websocket.
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'schedule_change_export_summary_%s' % self.request.id,
        {
            'type': 'schedule.export.summary',
            'task': self.request.id,
            'file_url': default_storage.url(saved_file),
        }
    )


def get_settings():
    settings_schedule = ScheduleChangeSettingsModel.objects.first()
    if not settings_schedule:
        # Create default settings.
        settings_schedule = ScheduleChangeSettingsModel.objects.create().save()

    return settings_schedule


def get_classes_from_display(flat_classes: str) -> QuerySet:
    classes_str = flat_classes.split(";")
    use_teaching_display = " — " in classes_str[0]
    classes_ids = []
    for cl in classes_str:
        classe = cl.split(" — ")[0] if use_teaching_display else cl
        year = classe[0]
        teaching = TeachingModel.objects.get(display_name=cl.split(" — ")[1])\
            if use_teaching_display else get_settings().teachings.all()[0]
        if "année" in classe:
            classes_ids += [cm.id for cm in ClasseModel.objects.filter(year=int(year), teaching=teaching)]
        else:
            classe_letter = classe[1:].lower()
            classes_ids.append(ClasseModel.objects.get(year=int(year), letter__iexact=classe_letter, teaching=teaching).id)

    return ClasseModel.objects.filter(pk__in=classes_ids)
