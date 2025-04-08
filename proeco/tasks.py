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
import time
import random

from celery import shared_task

from django.conf import settings

from .models import ProEcoWriteModel


@shared_task(bind=True)
def task_write_proeco(self, id):
    write_task = ProEcoWriteModel.objects.get(id=id)

    if not settings.SYNC_FDB or not isinstance(write_task.payload, list):
        write_task.status = ProEcoWriteModel.ERROR
        write_task.save()
        return

    if write_task.method == "set_student_absence":
        from fdb import DatabaseError

        from libreschoolfdb.writer import set_student_absence
        from libreschoolfdb import absences

        server = [
            s["server"]
            for s in settings.SYNC_FDB_SERVER
            if s["teaching_name"] == write_task.teaching.name
        ]

        if len(server) != 1:
            write_task.status = ProEcoWriteModel.ERROR
            write_task.save()
            return

        cursor = absences._get_absence_cursor(fdb_server=server[0])

        for data in write_task.payload:
            try:
                result = set_student_absence(
                    matricule=data["matricule"],
                    day=datetime.datetime.strptime(data["date"], "%Y-%m-%d").date(),
                    period=data["period"],
                    absence_status=data["absence_status"],
                    cur=cursor,
                    fdb_server=server[0],
                    commit=False,
                )
            except DatabaseError:
                # Wait and retry
                print("Wait and retry…")
                time.sleep(random.randint(10, 20))
                result = set_student_absence(
                    matricule=data["matricule"],
                    day=datetime.datetime.strptime(data["date"], "%Y-%m-%d").date(),
                    period=data["period"],
                    absence_status=data["absence_status"],
                    cur=cursor,
                    commit=False,
                )

            if not result:
                cursor.connection.rollback()
                write_task.status = ProEcoWriteModel.ERROR
                write_task.save()
                return

        cursor.connection.commit()
        cursor.connection.close()

        write_task.status = ProEcoWriteModel.DONE
        write_task.save()
