# Generated by Django 4.0.5 on 2022-10-05 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("proeco", "0002_templateselectionmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="overwritedatamodel",
            name="old_value",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="overwritedatamodel",
            name="uid",
            field=models.BigIntegerField(
                blank=True,
                help_text="Identifiant unique (matricule de l'étudiant ou du responsable).",
                null=True,
            ),
        ),
    ]
