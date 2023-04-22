# Generated by Django 2.2.3 on 2019-09-09 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("absence_prof", "0005_auto_20190909_1427"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absence",
            name="date_absence_end",
            field=models.DateField(
                default=datetime.datetime(2019, 9, 9, 15, 0, 54, 211430),
                verbose_name="Date de la fin de l'absence",
            ),
        ),
        migrations.AlterField(
            model_name="absence",
            name="date_absence_start",
            field=models.DateField(
                default=datetime.datetime(2019, 9, 9, 15, 0, 54, 211348),
                verbose_name="Date du début de l'absence",
            ),
        ),
        migrations.AlterField(
            model_name="absence",
            name="datetime_absence_end",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="date de la fin de l'absence"
            ),
        ),
        migrations.AlterField(
            model_name="absence",
            name="datetime_absence_start",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="date du début de l'absence"
            ),
        ),
    ]
