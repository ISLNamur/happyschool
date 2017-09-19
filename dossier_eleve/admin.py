from django.contrib import admin

from .models import CasEleve, InfoEleve, SanctionDecisionDisciplinaire

class CasDisciplinaireAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'datetime_encodage', 'info', 'sanction_decision', 'datetime_conseil', 'sanction_faite')

admin.site.register(CasEleve, CasDisciplinaireAdmin)
admin.site.register(InfoEleve)
admin.site.register(SanctionDecisionDisciplinaire)
