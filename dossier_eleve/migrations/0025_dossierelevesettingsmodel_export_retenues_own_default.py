# Generated by Django 4.0.5 on 2022-09-30 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dossier_eleve', '0024_rename_matricule_caseleve_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossierelevesettingsmodel',
            name='export_retenues_own_classes_default',
            field=models.BooleanField(default=False, help_text="Lors de l'export des retenues dans les demandes de sanction, la case pour\n        pour filter pour ses classes sera cochée par défaut."),
        ),
    ]
