from django.contrib import admin

from .models import (
    StudentAbsenceModel,
    StudentAbsenceSettingsModel,
    ClasseNoteModel,
    JustificationModel,
    PeriodModel,
)


class StudentAbsenceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "date_absence",
        "period",
        "is_absent",
    )


admin.site.register(StudentAbsenceSettingsModel)
admin.site.register(ClasseNoteModel)
admin.site.register(StudentAbsenceModel, StudentAbsenceAdmin)
admin.site.register(JustificationModel)
admin.site.register(PeriodModel)
