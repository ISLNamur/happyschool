# This file is part of Appyschool.
#
# Appyschool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# Appyschool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Appyschool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class, route

from core.consumers import SearchTeacherConsumer, SearchStudentsClassesYears, GetMenu
# from schedule_change.bindings import ScheduleChangeBinding


class APIDemultiplexer(WebsocketDemultiplexer):
    http_user_and_session = True

    consumers = {
        # 'schedule_change': ScheduleChangeBinding.consumer,
        'get_teachers': SearchTeacherConsumer,
        'get_students_classes_years': SearchStudentsClassesYears,
        'get_menu': GetMenu,
    }

    def connection_groups(self, **kwargs):
        return ['schedule_change']


from channels.routing import route
from myapp.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    # route("websocket.connect", ws_add),
    # route("websocket.receive", ws_message),
    # route("websocket.disconnect", ws_disconnect),
    route_class(APIDemultiplexer),
]
