# Generated by Django 4.2.16 on 2025-01-20 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_columntofieldimportmodel"),
        ("proeco", "0004_proecowritemodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="proecowritemodel",
            name="teaching",
            field=models.ForeignKey(
                default=None, on_delete=django.db.models.deletion.CASCADE, to="core.teachingmodel"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="proecowritemodel",
            name="method",
            field=models.CharField(max_length=30),
        ),
    ]
