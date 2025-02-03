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

import time

from django.core.management.base import BaseCommand

from proeco.models import ProEcoWriteModel
from proeco.tasks import task_write_proeco
from core.email import send_email

from django.conf import settings


class Command(BaseCommand):
    help = "Check ProEco write command."

    def add_arguments(self, parser):
        parser.add_argument("--try-again", action="store_true")
        parser.add_argument("--email", action="store_true")

    def handle(self, *args, **options):
        not_done_write = ProEcoWriteModel.objects.exclude(status=ProEcoWriteModel.DONE)

        for write in not_done_write:
            print(write)
            if options["try_again"]:
                task_write_proeco.delay(write.id)
                time.sleep(1)

        if options["email"]:
            send_email(
                to=settings.EMAIL_ADMIN,
                subject="Check proeco writes",
                email_template="proeco/warn_write.html",
                context={"write": not_done_write},
            )
