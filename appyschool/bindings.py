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

import json

from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from channels_api.bindings import ResourceBinding

from channels_api.settings import api_settings
from channels_api.decorators import list_action, detail_action
from channels_api.permissions import IsAuthenticated


class AppySchoolBinding(ResourceBinding):
    # The model must have a user and datetime_encodage fields.
    model = None
    stream = None
    serializer_class = None
    queryset = None
    # permission_classes = (IsAuthenticated,)
    channel_session_user = True

    default_order = None
    filters = ()
    filters_display = ()

    def perform_create(self, serializer):
        serializer.save(
            datetime_encodage=timezone.now(),
            user=self.message.user.username,
        )

    # Override list action to provide per page option.
    @list_action()
    def list(self, data, **kwargs):
        if not data:
            data = {}

        queryset = self.get_queryset()

        per_page = data.get('per_page', api_settings.DEFAULT_PAGE_SIZE)
        paginator = Paginator(queryset, per_page)
        page = data.get('page', 1)
        data = paginator.page(page)
        serializer = self.get_serializer(data, many=True)
        full_data = {
            'content': serializer.data,
            'page': page,
            'num_pages': paginator.num_pages,
            'total_count': paginator.count
        }
        return full_data, 200

    def get_queryset(self):
        content = json.loads(self.message.content['text'])
        if content['action'] == 'list' and content['data']:
            # Set order.
            order_by = content['data'].get('order_by', self.default_order)
            queryset = self.order_queryset(order_by)

            # Set filters.
            filters = content['data'].get('filters', {})
            for k, v in filters.items():
                queryset = self.set_filter_queryset(queryset, (k, v))
            return queryset

        return self.queryset.all()

    def order_queryset(self, order_by):
            return self.queryset.order_by(order_by)

    def set_filter_queryset(self, queryset, filter):
        str_converts = {'date_': "%Y-%m-%d", 'time_': '%H:%M', 'datetime-local_': "%Y-%m-%d, %H:%M"}
        if filter[0] in self.filters:
            q_obj = Q()
            for f in filter[1]:
                is_date = False
                for str_type, format_datetime in str_converts.items():
                    if filter[0].startswith(str_type):
                        dates = map(lambda d: timezone.datetime.strptime(d, format_datetime), f.split(" "))
                        q_obj |= Q(**{filter[0] + "__range": list(dates)})
                        is_date = True
                        break
                if not is_date:
                    q_obj |= Q(**{filter[0] + "__istartswith": f})
            return queryset.filter(q_obj)

        return queryset

    @list_action()
    def get_filters(self, data=None, **kwargs):
        filter_options = []
        for i in enumerate(self.filters):
            filter_options.append({'value': i[1], 'text': self.filters_display[i[0]]})
        return filter_options, 200

    @list_action()
    def get_filters_options(self, data=None, **kwargs):
        if len(data['query']) == 0:
            return [], 200

        queryset = self.get_queryset()
        results = queryset.filter(**{data['filter_type'] + '__startswith': data['query']}).values_list(data['filter_type'])
        results = list(map(lambda o: {'filterType': data['filter_type'], 'tag': o[0], 'value': data['filter_type'] + '-' + o[0]}, results))
        return results, 200
