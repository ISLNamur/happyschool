# Generated by Django 4.2 on 2023-10-12 12:52

from datetime import date

from django.db import migrations, models
import django.db.models.deletion


def move_to_other_adjustments_archive(apps, schema_editor):
    PIAModel = apps.get_model("pia", "PIAModel")
    OtherAdjustmentsModel = apps.get_model("pia", "OtherAdjustmentsModel")

    start_date = date(2023, 8, 28)
    end_date = date(2024, 7, 5)

    for pia in PIAModel.objects.all():
        other_adjustments = OtherAdjustmentsModel(
            pia_model=pia,
            date_start=start_date,
            date_end=end_date,
            other_adjustments=pia.other_adjustments,
        )
        other_adjustments.save()


class Migration(migrations.Migration):
    dependencies = [
        ("pia", "0033_scheduleadjustmentplanmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="OtherAdjustmentsModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("other_adjustments", models.TextField(blank=True)),
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
        migrations.AddConstraint(
            model_name="otheradjustmentsmodel",
            constraint=models.CheckConstraint(
                check=models.Q(("date_start__lte", models.F("date_end"))),
                name="other_adj_ensure_date_start_lte_date_end",
            ),
        ),
        migrations.RunPython(move_to_other_adjustments_archive),
    ]
