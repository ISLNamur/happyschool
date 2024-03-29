# Generated by Django 2.2.13 on 2020-08-26 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_auto_20200818_1441"),
    ]

    operations = [
        migrations.AddField(
            model_name="coresettingsmodel",
            name="school_city",
            field=models.CharField(default="", max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name="coresettingsmodel",
            name="school_fax",
            field=models.CharField(default="", max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name="coresettingsmodel",
            name="school_phone",
            field=models.CharField(default="", max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name="coresettingsmodel",
            name="school_postal_code",
            field=models.CharField(default="", max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name="coresettingsmodel",
            name="school_street",
            field=models.CharField(default="", max_length=200, blank=True),
        ),
    ]
