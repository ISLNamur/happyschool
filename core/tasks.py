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
import io
import json

from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.core.exceptions import ObjectDoesNotExist

from core.adminsettings.importclass import ImportStudentCSV
from core.models import TeachingModel


class WSImportStudentCSV(ImportStudentCSV):
    channel_layer = get_channel_layer()

    def __init__(self, teaching: TeachingModel, task_id: str, column_index: dict=None) -> None:
        super().__init__(teaching, column_index=column_index)
        self.task_id = task_id

    def print_log(self, log: str) -> None:
        async_to_sync(self.channel_layer.group_send)(
            'core_import_student_state_%s' % self.task_id,
            {
                'type': 'core.import.state',
                'task': self.task_id,
                'status': log,
            }
        )


@shared_task(bind=True)
def task_test(self, csv_file, teaching, columns, ignore_first_line):
    io_text = io.StringIO(csv_file)
    channel_layer = get_channel_layer()
    time.sleep(2)
    try:
        teaching_model = TeachingModel.objects.get(id=int(teaching))
    except ObjectDoesNotExist:
        async_to_sync(channel_layer.group_send)(
            'core_import_student_state_%s' % self.request.id,
            {
                'type': 'core.import.state',
                'task': self.request.id,
                'status': 'Teaching model does not exist!',
            }
        )
        return
    column_index = {j: int(i[-1]) for i, j in json.loads(columns).items()}
    import_student_csv = WSImportStudentCSV(teaching_model, self.request.id, column_index)
    import_student_csv.sync(io_text, ignore_first_line=ignore_first_line, has_header=False)
