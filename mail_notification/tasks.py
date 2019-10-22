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

from core.email import send_email_with_mg, send_email_with_sp
from core.people import People
from core.models import ResponsibleModel, StudentModel, ClasseModel, EmailModel

from mail_notification.models import EmailNotification, OtherEmailGroupModel, OtherEmailModel, EmailNotificationSettingsModel
from mail_answer.models import MailAnswerModel, MailTemplateModel
from mail_answer.models import MailAnswerSettingsModel as AnswersSettings
from mail_answer.tasks import task_sync_mail_answers


def get_settings():
    settings_email_notif = EmailNotificationSettingsModel.objects.first()
    if not settings_email_notif:
        # Create default settings.
        settings_email_notif = EmailNotificationSettingsModel.objects.create().save()

    return settings_email_notif


@shared_task(bind=True)
def task_send_emails_notif(self, pk, one_by_one=True, responsibles=True):
    """ Send emails """
    # First sync media between local and distant server
    subprocess.run(settings.EMAIL_ATTACHMENTS_SYNC['rsync_command'], shell=True)

    # Get EmailNotification object.
    email_notif = EmailNotification.objects.get(pk=pk)

    # Get recipients.
    recipients = [(email_notif.email_from.split("<")[1][:-1], None)] if "<" in email_notif.email_from else [email_notif.email_from]
    recipients += list(get_emails(email_notif.email_to, email_notif.to_type, email_notif.teaching, responsibles=responsibles,
                                  template=email_notif.answers, all_parents=True))

    # Add a carbon copy to recipients.
    settings_email_notif = get_settings()
    if email_notif.to_type == 'teachers':
        recipients += list(map(lambda e: (e.email, None), settings_email_notif.add_cc_teachers.all()))
    elif email_notif.to_type == 'parents':
        recipients += list(map(lambda e: (e.email, None), settings_email_notif.add_cc_parents.all()))

    # recipients += [(settings.EMAIL_ADMIN, None), ('directeur@isln.be', None), ('sous-directeur@isln.be', None)]
    if settings.DEBUG:
        print(recipients)

    # Get attachments.
    attachments = list(map(lambda a: a.attachment.path, email_notif.attachments.all()))
    # Log progress.
    email_notif.errors = "Submitting."
    email_notif.save()

    # Set template as used.
    if email_notif.answers:
        email_notif.answers.is_used = True
        email_notif.answers.save()

    if one_by_one:
        one_ok = False
        for r, a in recipients:
            email_body = "<html>%s</html>" % email_notif.body
            # Check if there is answer form attached to the email.
            if a:
                email_body = email_body.replace("specific_uuid", str(a.uuid))

            if not settings.DEBUG:
                response = send_email_with_sp([r],
                                   email_notif.subject,
                                   email_body,
                                   from_email=email_notif.email_from,
                                   attachments=attachments)

                if response.status_code != 200:
                    if settings.DEBUG:
                        print("Error with %s" % r)
                        print(response.json)
                        email_notif.errors += "Error w/ %s: %s |" % (r, response.status_code)
                        if len(email_notif.errors) > 9000:
                            break
                    break

                else:
                    one_ok = True
            time.sleep(2)
        if one_ok:
            email_notif.errors = email_notif.errors.replace("Submitting.", "")
            email_notif.errors += "Sent."

        # Send an email to admin
        if settings.DEBUG:
            send_email_with_sp([settings.EMAIL_ADMIN],
                               email_notif.subject,
                               "<html>%s<br>%s</html>" % (email_notif.body, recipients),
                               from_email=email_notif.email_from,
                               attachments=attachments)
    else:
        response = send_email_with_sp(recipients,
                                      email_notif.subject,
                                      "<html>%s</html>" % email_notif.body,
                                      from_email=email_notif.email_from,
                                      attachments=attachments)

        if response.status_code == 200:
            email_notif.errors = "Sent."
        else:
            email_notif.errors = "Error."

    email_notif.save()


def get_emails(email_to: list, to_type: str, teaching: str, responsibles: bool=True,
               template: MailTemplateModel=None, all_parents: bool=False) -> list():
    """
        Retrieve emails of the student's parent or teachers and responsibles.
    :param email_to: A list of keyword that might be classes, years, degree or a group of responsibles (2B, 1ère année,…).
    :param to_type: A string that specify which kind of recipients (teachers or parents).
    :param teaching: The teaching string.
    :param responsibles: Whether, when sending to teachers, responsibles need to be added (educators, coordonators,…).
    :param template: A MailTemplate model that implies the creation of a MailAnswer model for each student. Has no effect for teachers.
    :param all_parents: A boolean that indicates if all the parents or only the student's responsible need to be taking into account.
    :return: A list of emails in a tuple shape.
    """
    recipients = email_to.split(',')
    emails = []
    if to_type == 'teachers':
        email_school = get_settings().use_email_school
        for recip in recipients:
            # Check if it is the staff.
            if recip == 'Personnels':
                staff = ResponsibleModel.objects.filter(is_teacher=False, is_educator=False, is_secretary=False)
                emails += list(map(lambda s: (s.email, None), staff))
                continue
            # Check if it is a custom group.
            is_group = False
            for group in OtherEmailGroupModel.objects.all():
                if recip == group.name:
                    is_group = True
                    emails += list(map(lambda p: (p.email, None), OtherEmailModel.objects.filter(group=group.pk)))
                    break
            if is_group:
                continue

            # So it is directly related to classes.
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
                elif "Toutes les classes" in recip:
                    years += [1, 2, 3, 4, 5, 6]
                # elif "Tout le personnel" in recip:
                #
                else:
                    years = []
                classes = ClasseModel.objects.filter(year__in=years, teaching__name=teaching)

            teachers = ResponsibleModel.objects.filter(classe__in=classes, is_teacher=True)
            if responsibles:
                resp_email = EmailModel.objects.filter(years__in=years, teaching__name=teaching)
                emails += list(map(lambda e: (e.email, None), resp_email))

            emails += list(map(lambda t: (t.email_school if email_school else t.email, None), teachers))
        return set(emails)

    elif to_type == "parents":
        students = []
        # Collect students
        for recip in recipients:
            years = []
            # If it starts with a digit, it could be a class, a year or a degree.
            if recip[0].isdigit():
                # Class length is only two.
                if len(recip) == 2:
                    years = [int(recip[0])]
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         letter=recip[1].lower(),
                                                         teaching__name=teaching)
                elif 'année' in recip:
                    years = [int(recip[0])]
                    classes = ClasseModel.objects.filter(year=int(recip[0]),
                                                         teaching__name=teaching)
                else:
                    # It is a degrée
                    years = [int(recip[0]) * 2, int(recip[0]) * 2 - 1]
                    classes = ClasseModel.objects.filter(
                        year__in=years,
                        teaching__name=teaching)
            else:
                # It is a cycle.
                if "Cycle supérieur" in recip:
                    years = [4, 5, 6]
                elif "Cycle inférieur" in recip:
                    years = [1, 2, 3]
                elif "Toutes les classes" == recip:
                    print('toutes les classes')
                    years = [1, 2, 3, 4, 5, 6]
                else:
                    years = []
                classes = ClasseModel.objects.filter(year__in=years, teaching__name=teaching)

            if responsibles:
                resp_email = EmailModel.objects.filter(years__in=years, teaching__name=teaching)
                emails += list(map(lambda e: (e.email, None), resp_email))

            students += list(StudentModel.objects.filter(classe__in=classes))

        # Remove duplicates.
        students = set(students)

        def get_parents_email(student, to_resp=False):
            info = student.additionalstudentinfo
            parents_email = set()
            if to_resp:
                parents_email.add(info.resp_email)
            if all_parents:
                parents_email = parents_email.union({
                    info.mother_email,
                    info.father_email
                })

            # Remove None and empty values.
            return list(filter(lambda e: e is not None and e is not "", parents_email))

        # Attach for each student an AnswerModel (template case).
        if template:
            template.is_used = True
            template.save()
            students = list(map(lambda s: (s, MailAnswerModel(student=s, template=template)), students))
            MailAnswerModel.objects.bulk_create(map(lambda s: s[1], students))
            answers_settings = AnswersSettings.objects.first()
            if answers_settings.use_remote and not answers_settings.is_remote:
                task_sync_mail_answers.apply_async(countdown=2)
            for s, a in students:
                emails += list(map(lambda e: (e, a), get_parents_email(s)))
            return emails

        for s in students:
            emails += list(map(lambda e: (e, None), get_parents_email(s)))

        # Remove duplicates.
        return set(emails)
