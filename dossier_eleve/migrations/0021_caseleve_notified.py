# Generated by Django 2.2.24 on 2021-11-25 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dossier_eleve", "0020_auto_20211125_1058"),
    ]

    operations = [
        migrations.AddField(
            model_name="caseleve",
            name="notified",
            field=models.BooleanField(default=False),
        ),
    ]
