# Generated by Django 2.2.3 on 2019-10-24 13:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dossier_eleve", "0002_auto_20190910_1426"),
    ]

    operations = [
        migrations.AddField(
            model_name="dossierelevesettingsmodel",
            name="filter_teacher_entries_by_tenure",
            field=models.BooleanField(
                default=True,
                help_text="Si activé, seuls les titulaires peuvent voir les cas de leurs élèves.",
            ),
        ),
    ]
