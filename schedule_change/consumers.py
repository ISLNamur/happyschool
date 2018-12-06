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

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ExportSummaryConsumer(JsonWebsocketConsumer):

    def connect(self):
        celery_id = self.scope['url_route']['kwargs']['celery_id']
        self.group_name = 'schedule_change_export_summary_%s' % celery_id

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def schedule_export_summary(self, event):
        self.send_json({
            "task": event["task"],
            "file_url": event["file_url"],
        })
