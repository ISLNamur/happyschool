from rest_framework.renderers import JSONRenderer

from django.shortcuts import render

from .models import ScheduleChangeSettings
from .serializers import ScheduleChangeSettingsSerializer


def test(request):
    try:
        settings = ScheduleChangeSettings.objects.all()[0]
        json_settings = JSONRenderer().render(ScheduleChangeSettingsSerializer(settings).data)
    except IndexError:
        json_settings = {}

    return render(request, template_name="schedule_change/index.html", context={'app_settings': json_settings})
