# Generated by Django 2.2.2 on 2019-07-01 18:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_responsiblemodel_birth_date"),
        ("absence_prof", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="absence",
            name="comment",
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name="absence",
            name="datetime_encoding",
            field=models.DateTimeField(auto_now_add=True, verbose_name="date de l'encodage"),
        ),
        migrations.CreateModel(
            name="AbsenceProfSettingsModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("teachings", models.ManyToManyField(default=None, to="core.TeachingModel")),
            ],
        ),
    ]
