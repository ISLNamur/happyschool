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

from django.contrib import admin

from .models import LatenessModel, LatenessSettingsModel, SanctionTriggerModel, MailTemplateModel


class TriggerAdmin(admin.ModelAdmin):
    filter_horizontal = ("classe",)


admin.site.register(LatenessModel)
admin.site.register(LatenessSettingsModel)
admin.site.register(SanctionTriggerModel, TriggerAdmin)
admin.site.register(MailTemplateModel)
