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
from .models import StudentModel, TeachingModel, ResponsibleModel, AdditionalStudentInfo, \
    ClasseModel, EmailModel, YearModel, CoreSettingsModel, ImportCalendarModel, \
    CourseModel, GivenCourseModel, PeriodCoreModel, CourseScheduleModel, MenuEntryModel, \
    LevelModel, GroupLevelModel


class StudentCoreAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'last_name', 'first_name', 'classe',)
    search_fields = ['last_name', "first_name", 'matricule']
    list_filter = ["classe"]
    list_select_related = True
    ordering = ["classe__year", "classe__letter", "last_name", "first_name"]


class AdditionalStudentInfoCoreAdmin(admin.ModelAdmin):
    list_display = ["student", "resp_email", "mother_email", "father_email"]
    search_fields = ['student__last_name', "student__first_name", 'student__matricule']
    list_filter = ["student__classe"]
    ordering = [
        "student__classe__year", "student__classe__letter",
        "student__last_name", "student__first_name"
    ]


class InactivesListFilter(admin.SimpleListFilter):
    title = "Inactivité"

    parameter_name = 'inactives'

    def lookups(self, request, model_admin):
        return (
            ("actives", "Actifs"),
            ("inactives", "Inactifs"),
        )

    def queryset(self, request, queryset):
        if self.value() == "inactives":
            return queryset.filter(inactive_from__isnull=False)

        if self.value() == "actives":
            return queryset.filter(inactive_from__isnull=True)

        return queryset


class ResponsibleCoreAdmin(admin.ModelAdmin):
    list_display = [
        'matricule', 'last_name', 'first_name',
        'is_teacher', 'is_educator', 'is_secretary',
        'user'
    ]
    search_fields = ['last_name', "first_name", 'matricule']
    filter_horizontal = ('classe', 'tenure',)
    list_filter = ["is_teacher", "is_educator", "is_secretary", InactivesListFilter, ]
    autocomplete_fields = ["user"]


class ClassCoreAdmin(admin.ModelAdmin):
    ordering = ['teaching', 'year', 'letter']
    list_filter = ['year', 'letter', 'teaching']


admin.site.register(StudentModel, StudentCoreAdmin)
admin.site.register(TeachingModel)
admin.site.register(ResponsibleModel, ResponsibleCoreAdmin)
admin.site.register(AdditionalStudentInfo, AdditionalStudentInfoCoreAdmin)
admin.site.register(ClasseModel, ClassCoreAdmin)
admin.site.register(CourseModel)
admin.site.register(GivenCourseModel)
admin.site.register(EmailModel)
admin.site.register(YearModel)
admin.site.register(CoreSettingsModel)
admin.site.register(ImportCalendarModel)
admin.site.register(PeriodCoreModel)
admin.site.register(CourseScheduleModel)
admin.site.register(MenuEntryModel)
admin.site.register(LevelModel)
admin.site.register(GroupLevelModel)
