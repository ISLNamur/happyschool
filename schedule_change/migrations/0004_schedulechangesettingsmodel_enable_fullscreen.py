# Generated by Django 2.2.3 on 2019-10-17 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedule_change", "0003_auto_20190516_1433"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedulechangesettingsmodel",
            name="enable_fullscreen",
            field=models.BooleanField(default=False),
        ),
    ]
