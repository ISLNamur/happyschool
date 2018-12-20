from django.contrib import admin

from .models import StudentAbsenceModel, StudentAbsenceSettingsModel


class StudentAbsenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date_absence', 'morning', 'afternoon')


admin.site.register(StudentAbsenceSettingsModel)
admin.site.register(StudentAbsenceModel, StudentAbsenceAdmin)
