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


# from rest_framework.renderers import JSONRenderer
#
# from django.shortcuts import render

# from .models import ScheduleChangeSettings
# from .serializers import ScheduleChangeSettingsSerializer
#
#
# def test(request):
#     try:
#         settings = ScheduleChangeSettings.objects.all()[0]
#         json_settings = JSONRenderer().render(ScheduleChangeSettingsSerializer(settings).data)
#     except IndexError:
#         json_settings = {}
#
#     return render(request, template_name="schedule_change/index.html", context={'app_settings': json_settings})
