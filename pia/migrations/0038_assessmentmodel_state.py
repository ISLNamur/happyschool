# Generated by Django 4.2 on 2024-03-11 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pia", "0037_selecteddisorderresponsenewmodel_custom_response_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessmentmodel",
            name="state",
            field=models.CharField(
                choices=[
                    ("OK", "Objectif atteint"),
                    ("NOK", "Objectif non-atteint"),
                    ("IP", "En cours"),
                ],
                default="OK",
                max_length=4,
            ),
        ),
        migrations.RemoveField(
            model_name="branchgoalmodel",
            name="validated",
        ),
        migrations.RemoveField(
            model_name="crossgoalmodel",
            name="validated",
        ),
    ]
