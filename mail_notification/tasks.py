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

import subprocess
import time

from django.conf import settings

from celery import shared_task

from core.email import send_email_with_mg
from core.people import People
from core.models import ResponsibleModel, StudentModel, ClasseModel, EmailModel

from mail_notification.models import EmailNotification


@shared_task(bind=True)
def task_send_emails_notif(self, pk, to_type, teaching="secondaire", one_by_one=True, responsibles=True):
    """ Send emails """
    # First sync media between local and distant server
    subprocess.run(settings.MEDIA_SYNC['rsync_command'], shell=True)
    email_notif = EmailNotification.objects.get(pk=pk)
    print(email_notif)
    recipients = list(get_emails(email_notif.email_to, to_type, teaching, responsibles=responsibles))
    recipients += ['manuel.tondeur@isln.be', 'directeur@isln.be', 'sous-directeur@isln.be']
    print(recipients)
    if settings.DEBUG:
        recipients = [settings.EMAIL_ADMIN]

    attachments = list(map(lambda a: a.attachment.path, email_notif.attachments.all()))
    email_notif.errors = "Submitting."
    email_notif.save()
    if one_by_one:
        one_ok = False
        print(attachments)
        for r in recipients:
            response = send_email_with_mg([r],
                               email_notif.subject,
                               "<html>%s</html>" % email_notif.body,
                               from_email=email_notif.email_from,
                               attachments=attachments)
            if response.status_code != 200:
                email_notif.errors += "Error with %s." % r
            else:
                one_ok = True
            time.sleep(0.4)
        if one_ok:
            email_notif.errors = email_notif.errors.replace("Submitting.", "")
            email_notif.errors += "Sent."
    else:
        response = send_email_with_mg(recipients,
                                      email_notif.subject,
                                      "<html>%s</html>" % email_notif.body,
                                      from_email=email_notif.email_from,
                                      attachments=attachments)

        if response.status_code == 200:
            email_notif.errors = "Sent."
        else:
            email_notif.errors = "Error."

    email_notif.save()


def get_emails(email_to, to_type, teaching="secondaire", responsibles=True):
    recipients = email_to.split(',')
    emails = []
    if to_type == 'teachers':
        for recip in recipients:
            years = []
            # If it starts with a digit, it could be a class, a year or a degree.
            if recip[0].isdigit():
                # Class length is only two.
                if len(recip) == 2:
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         letter=recip[1].lower(),
                                                         teaching__name=teaching)
                    years.append(int(recip[0]))
                elif 'année' in recip:
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         teaching__name=teaching)
                    years.append(int(recip[0]))
                else:
                    # It is a degrée.
                    classes = ClasseModel.objects.filter(year__in=[int(recip[0]) * 2, int(recip[0]) * 2 - 1],
                                                         teaching__name=teaching)
                    degree = int(recip[0])
                    years += [degree * 2, degree * 2 - 1]
            else:
                # It is a cycle.
                if "supérieur" in recip:
                    years += [4, 5, 6]
                elif "inférieur" in recip:
                    years += [1, 2, 3]
                elif "Tous les professeurs" in recip:
                    years += [1, 2, 3, 4, 5, 6]
                # elif "Tout le personnel" in recip:
                #
                else:
                    years = []
                classes = ClasseModel.objects.filter(year__in=years, teaching__name=teaching)

            teachers = ResponsibleModel.objects.filter(classe__in=classes, is_teacher=True)
            if responsibles:
                resp_email = EmailModel.objects.filter(years__in=years, teaching__name=teaching)
                emails += list(map(lambda e: e.email, resp_email))

            emails += list(map(lambda t: t.email_alias, teachers))
        return set(emails)

    elif to_type == "parents":
        for recip in recipients:
            # If it starts with a digit, it could be a class, a year or a degree.
            if recip[0].isdigit():
                # Class length is only two.
                if len(recip) == 2:
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         letter=recip[1].lower(),
                                                         teaching__name=teaching)
                elif 'année' in recip:
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         teaching__name=teaching)
                else:
                    # It is a degrée
                    classes = ClasseModel.objects.filter(
                        year__in=[int(recip[0]) * 2, int(recip[0]) * 2 - 1],
                        teaching__name=teaching)
            else:
                # It is a cycle.
                if "supérieur" in recip:
                    years = [4, 5, 6]
                elif "inférieur" in recip:
                    years = [1, 2, 3]
                elif "Tous" in recip:
                    years = [1, 2, 3, 4, 5, 6]
                else:
                    years = []
                classes = ClasseModel.objects.filter(year__in=years, teaching__name=teaching)

            students = StudentModel.objects.filter(classe__in=classes)
            for s in students:
                info = s.get_additional_info()
                parents_email = {info['resp_email'] if 'resp_email' in info else None,
                                 info['mother_email'] if 'mother_email' in info else None,
                                 info['father_email'] if 'father_email' in info else None,}
                parents = list(filter(lambda e: e is not None, parents_email))
                if len(parents) > 0:
                    emails += parents
        return list(set(emails))
