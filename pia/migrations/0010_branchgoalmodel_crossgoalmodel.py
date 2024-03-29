# Generated by Django 2.2.8 on 2020-03-02 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_auto_20200119_2055"),
        ("pia", "0009_auto_20200302_1200"),
    ]

    operations = [
        migrations.CreateModel(
            name="CrossGoalModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("indicator_action", models.TextField(blank=True)),
                ("given_help", models.TextField(blank=True)),
                ("self_assessment", models.CharField(blank=True, max_length=2000)),
                ("datetime_creation", models.DateTimeField(auto_now_add=True)),
                ("datetime_update", models.DateTimeField(auto_now=True)),
                ("cross_goals", models.CharField(max_length=2000)),
                (
                    "assessment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pia.AssessmentModel",
                    ),
                ),
                (
                    "pia_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pia.PIAModel"
                    ),
                ),
                ("responsible", models.ManyToManyField(blank=True, to="core.ResponsibleModel")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BranchGoalModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("indicator_action", models.TextField(blank=True)),
                ("given_help", models.TextField(blank=True)),
                ("self_assessment", models.CharField(blank=True, max_length=2000)),
                ("datetime_creation", models.DateTimeField(auto_now_add=True)),
                ("datetime_update", models.DateTimeField(auto_now=True)),
                ("branch_goals", models.CharField(max_length=2000)),
                ("parent_commitment", models.TextField(blank=True)),
                (
                    "assessment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pia.AssessmentModel",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pia.BranchModel",
                    ),
                ),
                (
                    "pia_model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="pia.PIAModel"
                    ),
                ),
                ("responsible", models.ManyToManyField(blank=True, to="core.ResponsibleModel")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
