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

import datetime

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from core.utilities import get_current_scholar_year_interval
from core.models import ParentNotificationSettingsModel
from core.email import send_email, get_resp_emails
from lateness.models import LatenessModel
from student_absence_teacher.models import StudentAbsenceTeacherModel


class Command(BaseCommand):
    help = "Send emails to parent that asked for."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Just show objects that will be removed; don't actually remove them.",
        )

    def handle(self, *args, **options):
        today = datetime.datetime.now()
        one_week_before = today - datetime.timedelta(days=6)
        print(f"Looking from {one_week_before}.")

        for setting in ParentNotificationSettingsModel.objects.all():
            context = {}

            context["student"] = setting.student

            context["latenesses"] = LatenessModel.objects.filter(
                datetime_creation__gte=one_week_before, student=setting.student
            )

            scholar_year_start, _ = get_current_scholar_year_interval()
            context["lateness_count"] = LatenessModel.objects.filter(
                student=setting.student,
                datetime_creation__gte=scholar_year_start,
            )

            context["exclusions"] = StudentAbsenceTeacherModel.objects.filter(
                date_absence__gte=one_week_before,
                student=setting.student,
                status=StudentAbsenceTeacherModel.EXCLUDED,
            )

            if context["latenesses"].exists() or context["exclusions"].exists():
                print(f"{setting.student} | sending mails to {setting.contact}")
                print(
                    f"Latenesses: {context['latenesses'].count()}, Exclusions: {context['exclusions'].count()}"
                )

                resp_emails = get_resp_emails(setting.student)

                send_email(
                    setting.contact,
                    "Récapitulatif hebdomadaire",
                    "core/parent_notification_email.html",
                    context=context,
                    reply_to=resp_emails,
                )
