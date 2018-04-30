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

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .serializers import MailTemplateSerializer, MailAnswerSerializer, ChoiceSerializer, OptionSerializer
from .models import MailTemplateModel, MailAnswerModel, ChoiceModel, OptionModel


permissions = (IsAuthenticated, DjangoModelPermissions,)


class OptionViewSet(ModelViewSet):
    queryset = OptionModel.objects.all()
    serializer_class = OptionSerializer
    permission_classes = permissions


class ChoiceViewSet(ModelViewSet):
    queryset = ChoiceModel.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = permissions


class MailTemplateViewSet(ModelViewSet):
    queryset = MailTemplateModel.objects.all()
    serializer_class = MailTemplateSerializer
    permission_classes = permissions


class MailAnswerViewSet(ModelViewSet):
    queryset = MailAnswerModel.objects.all()
    serializer_class = MailAnswerSerializer
    permission_classes = permissions
