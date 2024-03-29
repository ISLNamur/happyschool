# Generated by Django 4.2 on 2023-05-25 06:50

from django.db import migrations, models
import django.db.models.deletion


def move_to_selected_disorder_response(apps, schema_editor):
    PIAModel = apps.get_model("pia", "PIAModel")
    SelectedDisorderResponseModel = apps.get_model("pia", "SelectedDisorderResponseModel")

    for pia in PIAModel.objects.all():
        for d_r in pia.disorder_response.all():
            for cat in d_r.categories.all():
                selected_disorder_response = SelectedDisorderResponseModel(
                    disorder_response=d_r, category=cat
                )
                selected_disorder_response.save()
                pia.selected_disorder_response.add(selected_disorder_response)


class Migration(migrations.Migration):
    dependencies = [
        ("pia", "0029_piamodel_datetime_created_piamodel_datetime_updated"),
    ]

    operations = [
        migrations.CreateModel(
            name="SelectedDisorderResponseModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pia.disorderresponsecategorymodel",
                    ),
                ),
                (
                    "disorder_response",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pia.disorderresponsemodel"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="piamodel",
            name="selected_disorder_response",
            field=models.ManyToManyField(blank=True, to="pia.selecteddisorderresponsemodel"),
        ),
        migrations.RunPython(move_to_selected_disorder_response),
        migrations.RemoveField(
            model_name="piamodel",
            name="disorder_response",
        ),
    ]
