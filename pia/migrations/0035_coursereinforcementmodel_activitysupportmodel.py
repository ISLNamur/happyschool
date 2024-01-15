# Generated by Django 4.2 on 2023-12-18 12:09
from datetime import date

from django.db import migrations, models
import django.db.models.deletion


def move_to_activity_support_archive(apps, schema_editor):
    PIAModel = apps.get_model("pia", "PIAModel")
    ActivitySupportModel = apps.get_model("pia", "ActivitySupportModel")

    start_date = date(2023, 8, 28)
    end_date = date(2024, 7, 5)

    for pia in PIAModel.objects.filter(advanced=False):
        # Check if there is ongoing support.
        for support in pia.support_activities.items():
            if len(support[1]["branch"]) > 0 or len(support[1]["teachers"]) > 0:
                support_activities = ActivitySupportModel(
                    pia_model=pia,
                    date_start=start_date,
                    date_end=end_date,
                    support_activities=pia.support_activities,
                )
                support_activities.save()
                break


class Migration(migrations.Migration):
    dependencies = [
        ("pia", "0034_otheradjustmentsmodel_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseReinforcementModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_updated", models.DateTimeField(auto_now=True)),
                ("branches", models.ManyToManyField(blank=True, to="pia.branchmodel")),
                (
                    "pia_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pia.piamodel"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ActivitySupportModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("support_activities", models.JSONField(default=dict)),
                ("directed_study", models.JSONField(default=dict)),
                ("datetime_created", models.DateTimeField(auto_now_add=True)),
                ("datetime_updated", models.DateTimeField(auto_now=True)),
                (
                    "pia_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pia.piamodel"
                    ),
                ),
            ],
        ),
        migrations.RunPython(move_to_activity_support_archive),
    ]