# Generated by Django 2.2.24 on 2021-11-26 14:22

from django.db import migrations, models


def migrate_datetime_sanction(apps, schema_editor):
    CasEleve = apps.get_model("dossier_eleve", "CasEleve")
    for cas in CasEleve.objects.all():
        if cas.datetime_sanction:
            cas.date_sanction = cas.datetime_sanction.date()
            cas.time_sanction_start = cas.datetime_sanction.time()
            cas.save()


class Migration(migrations.Migration):
    dependencies = [
        ("dossier_eleve", "0021_caseleve_notified"),
    ]

    operations = [
        migrations.AddField(
            model_name="caseleve",
            name="date_sanction",
            field=models.DateField(blank=True, null=True, verbose_name="Date de la sanction"),
        ),
        migrations.AddField(
            model_name="caseleve",
            name="time_sanction_start",
            field=models.TimeField(
                blank=True, null=True, verbose_name="Heure de début de la sanction"
            ),
        ),
        migrations.RunPython(migrate_datetime_sanction),
    ]
