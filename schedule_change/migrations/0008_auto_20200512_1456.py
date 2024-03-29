# Generated by Django 2.2.11 on 2020-05-12 12:56

from django.db import migrations
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    ScheduleChangeTypeModel = apps.get_model("schedule_change", "ScheduleChangeTypeModel")
    ScheduleChangeCategoryModel = apps.get_model("schedule_change", "ScheduleChangeCategoryModel")
    ScheduleChangePlaceModel = apps.get_model("schedule_change", "ScheduleChangePlaceModel")

    if ScheduleChangeTypeModel.objects.count() == 0:
        call_command("loaddata", "schedule_change_types", app_label="schedule_change")

    if ScheduleChangeCategoryModel.objects.count() == 0:
        call_command("loaddata", "schedule_change_categories", app_label="schedule_change")

    if ScheduleChangePlaceModel.objects.count() == 0:
        call_command("loaddata", "schedule_change_places", app_label="schedule_change")


class Migration(migrations.Migration):
    dependencies = [
        ("schedule_change", "0007_auto_20200512_1210"),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
