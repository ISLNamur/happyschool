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

from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models import TeachingModel

from .models import TemplateSelectionModel, ProEcoWriteModel
from .tasks import task_write_proeco


class ExportStudentSelectionAPI(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, format=None, **kwargs):
        """
        Defines the API endpoint to fetch student selections.

        :return: A response object with the generated file.
        """

        # Get a list of students by matricules
        matricules = set(self._get_student_list(request, kwargs))

        # Initialize template model
        template_model = TemplateSelectionModel.objects.first()

        # Generate text content with student selections
        matricules_text = ["MATRICS%i=%i=" % (i + 1, a) for (i, a) in enumerate(matricules)]
        text = template_model.template.replace("{matricules}", "\n".join(matricules_text))

        # Create response object with attachment content and file name
        response = HttpResponse(text, content_type="text/plain")
        response["Content-Disposition"] = (
            f'attachment; filename="{self._format_file_name(request, **kwargs)}"'
        )

        return response


def _get_student_list(self, request, **kwargs):
    """
    Fetches a list of students by their matricules.

    :param request: HTTP request object
    :return: A set of student matricules.
    """

    pass


def _format_file_name(self, request, **kwargs):
    return "Pref_NOMS_.TXT"


def proeco_write(
    app: str, method: str, payload: list, person: str, user: User, teaching: TeachingModel
):
    """
    Create and save a new ProEcoWriteModel instance, then apply the task to Celery's queue.

    :param app: The name of the django application.
    :param method: The name of the libreschoolfdb method.
    :param payload: The data to be written.
    :param person: The type of the person involved (student or teacher).
    :param user: The current user.
    :param teaching: A model representing a teaching model from example_app import proeco_write
    """
    write = ProEcoWriteModel(
        app=app, method=method, payload=payload, person=person, user=user, teaching=teaching
    )
    write.save()

    # Asynchronously process the write operation with a 2-second countdown
    task_write_proeco.apply_async(args=(write.id,), countdown=2)
