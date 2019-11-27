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
from .models import StudentModel, TeachingModel, ResponsibleModel, AdditionalStudentInfo,\
    ClasseModel, EmailModel, YearModel, CoreSettingsModel, ImportCalendarModel


class StudentCoreAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'last_name', 'first_name', 'classe',)
    search_fields = ['last_name', 'matricule']


class ResponsibleCoreAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'last_name', 'first_name', 'is_teacher', 'is_educator', 'is_secretary', 'user',)
    search_fields = ['last_name', 'matricule']
    filter_horizontal = ('classe','tenure',)



admin.site.register(StudentModel, StudentCoreAdmin)
admin.site.register(TeachingModel)
admin.site.register(ResponsibleModel, ResponsibleCoreAdmin)
admin.site.register(AdditionalStudentInfo)
admin.site.register(ClasseModel)
admin.site.register(EmailModel)
admin.site.register(YearModel)
admin.site.register(CoreSettingsModel)
admin.site.register(ImportCalendarModel)
