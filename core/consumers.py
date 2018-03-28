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

from channels.generic.websockets import JsonWebsocketConsumer
from django.conf import settings

from . import people


class GetMenu(JsonWebsocketConsumer):
    http_user = True
    action = "get_menu"

    def receive(self, content, multiplexer, **kwargs):
        active = content.get('active', None)
        apps = {
            'annuaire': {"display": "Annuaire", "url": "/annuaire", "active": "annuaire" == active},
        }

        if 'schedule_change' in settings.INSTALLED_APPS:
            apps['schedule_change'] = {"display": "Changements d'horaires", "url": "/schedule_change", "active": "schedule_change" == active}

        multiplexer.send({'action': self.action, "menu": apps})


class BaseSearchConsumer(JsonWebsocketConsumer):
    http_user = True
    action = None

    def receive(self, content, multiplexer, **kwargs):
        query = content.get('query', '')
        teaching = content.get('teaching', ["default"])
        context = content.get("context", "from_nowhere")

        result = self.search(query, teaching, context)
        multiplexer.send({'action': self.action, "result": result, "context": context})
        return

    def search(self, query, teaching, context):
        pass


class SearchTeacherConsumer(BaseSearchConsumer):
    action = "search_teachers"

    def search(self, query, teaching, context):
        if not query:
            return []

        if not teaching:
            teachers = people.People().get_teachers_by_name(query)
        else:
            teachers = people.People().get_teachers_by_name(query, teaching)

        return list(map(lambda t: str(t), teachers))


class SearchStudentsClassesYears(BaseSearchConsumer):
    action = "search_students_classes_years"

    def search(self, query, teaching, context):

        if len(query) == 0 or not query[0].isdigit():
            return []

        years = filter(lambda y: y == int(query[0]), people.get_years(teaching))
        def format_year(year):
            if year == 1:
                return "1ères"
            return str(year) + "èmes"

        years = list(map(format_year, years))

        classes = people.get_classes(teaching).filter(year=int(query[0]))

        if len(query) > 1:
            classes = classes.filter(letter=query[1])

        return years + list(map(lambda c: str(c), classes))
