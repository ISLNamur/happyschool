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

from rest_framework import serializers
from mail_notification.models import (
    EmailNotification,
    EmailAttachment,
    EmailSender,
    OtherEmailModel,
    OtherEmailGroupModel,
)


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = "__all__"
        depth = 1


class EmailSenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailSender
        fields = ["sender_email", "sender_email_name"]


class EmailAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = "__all__"


class OtherEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherEmailModel
        fields = "__all__"


class OtherEmailGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherEmailGroupModel
        fields = "__all__"
