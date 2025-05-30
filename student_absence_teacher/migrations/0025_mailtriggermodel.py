# Generated by Django 4.2.20 on 2025-05-26 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student_absence_teacher", "0024_studentabsenceteachersettingsmodel_can_see_exclusion"),
    ]

    operations = [
        migrations.CreateModel(
            name="MailTriggerModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("exclusion_count_trigger", models.PositiveSmallIntegerField(default=3)),
            ],
        ),
    ]
