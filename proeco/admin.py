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

from . import models


class OverwriteDataAdmin(admin.ModelAdmin):
    list_display = (
        "uid",
        "field",
        "value",
    )


class ProEcoWriteAdmin(admin.ModelAdmin):
    list_display = ("app", "method", "status", "datetime_creation")
    list_filter = ["status"]


admin.site.register(models.OverwriteDataModel, OverwriteDataAdmin)
admin.site.register(models.TemplateSelectionModel)
admin.site.register(models.ProEcoWriteModel, ProEcoWriteAdmin)
