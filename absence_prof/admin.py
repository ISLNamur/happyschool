from django.contrib import admin

from .models import MotifAbsence, Absence

admin.site.register(Absence)
admin.site.register(MotifAbsence)
