# Generated by Django 3.2.11 on 2022-01-31 13:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_auto_20220131_0954"),
    ]

    operations = [
        migrations.AddField(
            model_name="courseschedulemodel",
            name="place",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
