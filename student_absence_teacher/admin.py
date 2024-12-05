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

from .models import (
    StudentAbsenceTeacherModel,
    StudentAbsenceEducModel,
    StudentAbsenceTeacherSettingsModel,
    PeriodModel,
    LessonModel,
    JustificationModel,
    JustMotiveModel,
    MailTemplateModel,
)


class StudentEducAbsenceAdmin(admin.ModelAdmin):
    search_fields = ["student__last_name", "student__first_name"]
    list_filter = ["status"]
    ordering = ["-date_absence"]
    raw_id_fields = ["student"]
    list_display = (
        "student",
        "date_absence",
        "period",
        "status",
        "mail_warning",
    )


class StudentAbsenceTeacherAdmin(admin.ModelAdmin):
    raw_id_fields = ["student", "given_course"]
    list_filter = ["status"]


class JustificationAdmin(admin.ModelAdmin):
    raw_id_fields = ["student", "absences"]


admin.site.register(StudentAbsenceTeacherSettingsModel)
admin.site.register(PeriodModel)
admin.site.register(LessonModel)
admin.site.register(StudentAbsenceTeacherModel, StudentAbsenceTeacherAdmin)
admin.site.register(StudentAbsenceEducModel, StudentEducAbsenceAdmin)
admin.site.register(JustificationModel, JustificationAdmin)
admin.site.register(JustMotiveModel)
admin.site.register(MailTemplateModel)
