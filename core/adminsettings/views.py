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

import json
import csv

from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from core.utilities import get_menu
from core.tasks import task_test
from io import StringIO


class AdminView(LoginRequiredMixin,
                PermissionRequiredMixin,
                TemplateView):
    permission_required = ('core.add_responsible_model',)
    template_name = "core/admin/admin.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['menu'] = json.dumps(get_menu(self.request.user))
        return context


class TestFileAPIView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None) -> Response:
        ignore_first_line = request.POST.get("ignore_first_line", "false") == "true"
        file_obj = request.FILES['file']
        buffer = StringIO(file_obj.read().decode("utf-8-sig"))
        file_obj.seek(0)
        dialect = csv.Sniffer().sniff(file_obj.read(8192).decode("utf-8-sig"))
        reader = csv.reader(buffer, dialect)
        if ignore_first_line:
            next(reader, None)

        rows = []
        for row in reader:
            rows.append({'col%i' % i: x for i, x in enumerate(row)})
            if reader.line_num > 10:
                break

        return Response(data=json.dumps(rows), status=status.HTTP_200_OK)


class ImportStudentAPIView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        csv_text = request.FILES['file'].read().decode("utf-8-sig")
        teaching = request.POST.get('teaching', None)
        columns = request.POST.get('columns', '{}')
        ignore_first_line = json.loads(request.POST.get('ignore_first_line'))
        print(teaching)
        print(columns)
        if not teaching:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Teaching needed.")

        task = task_test.delay(csv_text, teaching, columns, ignore_first_line)
        print(task)
        return Response(data=json.dumps(str(task)), status=status.HTTP_200_OK)
