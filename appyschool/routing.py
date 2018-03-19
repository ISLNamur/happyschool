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
