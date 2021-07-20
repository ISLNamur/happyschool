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

from django import template
from django.core.exceptions import ObjectDoesNotExist

from core.models import ResponsibleModel
from core.serializers import GivenCourseSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def list_user_properties(context):
    if context['user'].is_anonymous:
        return "null"
    try:
        responsible = ResponsibleModel.objects.get(user=context['user'])
        given_courses_serialized = GivenCourseSerializer(responsible.courses.all(), many=True)
        return {
            "matricule": responsible.matricule,
            "teaching": [t.id for t in responsible.teaching.all()],
            "classes": [c.id for c in responsible.classe.all()],
            "given_courses": json.dumps(given_courses_serialized.data),
            "tenure": [t.id for t in responsible.tenure.all()],
        }
    except ObjectDoesNotExist:
        return ""
