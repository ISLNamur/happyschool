# Generated by Django 2.2.3 on 2019-10-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedule_change", "0004_schedulechangesettingsmodel_enable_fullscreen"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedulechangesettingsmodel",
            name="enable_fullscreen",
            field=models.BooleanField(
                default=False,
                help_text="Permet d'accéder à la page principale en lecture avec l'adresse /schedule_change/fullscreen/ et ce sans authentification",
            ),
        ),
    ]
