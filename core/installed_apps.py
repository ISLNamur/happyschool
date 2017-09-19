from django.conf import settings


def installed_apps(request):
    return {
        'app_infoeleve': 'infoeleve' in settings.INSTALLED_APPS,
        'app_infirmerie': 'infirmerie' in settings.INSTALLED_APPS,
        'app_absences': 'absence_prof' in settings.INSTALLED_APPS,
        'app_dossier_eleve': 'dossier_eleve' in settings.INSTALLED_APPS,
        'app_appels': 'appels' in settings.INSTALLED_APPS,
    }
