# Generated by Django 2.2.8 on 2020-01-08 09:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("student_absence", "0005_auto_20191226_1421"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentabsencemodel",
            name="afternoon",
        ),
        migrations.RemoveField(
            model_name="studentabsencemodel",
            name="morning",
        ),
    ]
