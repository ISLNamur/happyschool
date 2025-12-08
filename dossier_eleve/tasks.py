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

from datetime import date

from celery import shared_task

from django.conf import settings

from core.email import send_email
from core.models import ResponsibleModel, EmailModel
from core.utilities import get_scholar_year
from core.people import get_teachers_from_student
from core.views import get_core_settings

from .models import CasEleve, DossierEleveSettingsModel


@shared_task(bind=True)
def notify_sanction(self, instance_id):
    instance = CasEleve.objects.get(id=instance_id)
    student = instance.student
    context = {"student": student, "sanction": instance}
    core_settings = get_core_settings()

    for notify in instance.sanction_decision.notify.all():
        recipient = []
        # Check if we match the frequency.
        scholar_year_start = date(
            year=get_scholar_year(),
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        scholar_year_end = date(
            year=get_scholar_year() + 1,
            month=core_settings.month_scholar_year_start,
            day=core_settings.day_scholar_year_start,
        )
        sanction_count = CasEleve.objects.filter(
            datetime_encodage__gte=scholar_year_start,
            datetime_encodage__lt=scholar_year_end,
            student=student,
            sanction_decision=instance.sanction_decision,
        ).count()
        if sanction_count % notify.frequency != 0:
            continue

        if notify.recipient == "PA":
            if student.additionalstudentinfo.father_email:
                recipient.append(student.additionalstudentinfo.father_email)
            if student.additionalstudentinfo.mother_email:
                recipient.append(student.additionalstudentinfo.mother_email)
        elif notify.recipient == "LR":
            if student.additionalstudentinfo.resp_email:
                recipient.append(student.additionalstudentinfo.resp_email)
        elif notify.recipient == "SR":
            emails = EmailModel.objects.filter(teaching=student.teaching, years=student.classe.year)
            recipient += [e.email for e in emails]

        send_email(
            to=recipient,
            subject="Sanction concernant %s" % student.fullname,
            email_template="dossier_eleve/email_sanction.html",
            context=context,
        )


@shared_task(bind=True)
def task_send_info_email(self, instance_id):
    instance = CasEleve.objects.get(id=instance_id)
    student = instance.student
    teachers_obj = get_teachers_from_student(student)
    dossier_eleve_settings = DossierEleveSettingsModel.objects.first()

    teachers = [
        t.email_school if dossier_eleve_settings.use_school_email else t.email for t in teachers_obj
    ]
    context = {"student": student, "info": instance, "info_type": instance.info.info}

    # Add coord and educs to email list
    teachers += map(
        lambda e: e.email,
        EmailModel.objects.filter(teaching=student.teaching, years=student.classe.year),
    )
    teachers += list(map(lambda e: e.email, EmailModel.objects.filter(is_pms=True)))

    teachers = [t for t in teachers if t]

    if not settings.DEBUG:
        try:
            send_email(
                to=teachers,
                subject="ISLN : À propos de " + student.fullname_classe,
                email_template="dossier_eleve/email_info.html",
                context=context,
                attachments=instance.attachments.all(),
                use_bcc=True,
            )
        except Exception as err:
            send_email(
                to=teachers,
                subject="ISLN : À propos de " + student.fullname_classe,
                email_template="dossier_eleve/email_info.html",
                context=context,
                attachments=instance.attachments.all(),
                use_bcc=True,
            )
    else:
        print(teachers)
        send_email(
            to=[settings.EMAIL_ADMIN],
            subject="ISLN : À propos de " + student.fullname_classe,
            email_template="dossier_eleve/email_info.html",
            context=context,
            attachments=instance.attachments.all(),
        )
        for t in teachers:
            print(f"Sending email to : {str(t)}")
