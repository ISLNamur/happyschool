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

from happyschool.bindings import HappySchoolBinding
from schedule_change.models import ScheduleChange
from schedule_change.serializers import ScheduleChangeSerializer


class ScheduleChangeBinding(HappySchoolBinding):
    model = ScheduleChange
    stream = "schedule_change"
    serializer_class = ScheduleChangeSerializer
    queryset = ScheduleChange.objects.all()

    default_order = 'date_start'
    filters = ('teachers', 'date_start', 'date_end', 'classes')
    filters_display = ('Professeurs', 'Date de début', 'Date de fin', 'Classes')

    def order_queryset(self, order_by):
        if order_by == 'date_start':
            return self.queryset.order_by(order_by, 'time_start')
        else:
            return super(ScheduleChange).order_queryset(order_by)
