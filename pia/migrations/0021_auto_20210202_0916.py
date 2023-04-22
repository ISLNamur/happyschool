# Generated by Django 2.2.13 on 2021-02-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pia", "0020_crossgoalmodel_branches"),
    ]

    operations = [
        migrations.AddField(
            model_name="branchgoalmodel",
            name="validated",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="crossgoalmodel",
            name="validated",
            field=models.BooleanField(default=False),
        ),
    ]
