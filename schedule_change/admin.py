from django.contrib import admin

from .models import ScheduleChange, ScheduleChangeSettings


admin.site.register(ScheduleChange)
admin.site.register(ScheduleChangeSettings)
