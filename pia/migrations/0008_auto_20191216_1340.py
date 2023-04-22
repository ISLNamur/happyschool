# Generated by Django 2.2.8 on 2019-12-16 12:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pia", "0007_auto_20191212_0907"),
    ]

    operations = [
        migrations.AlterField(
            model_name="branchstatementmodel",
            name="difficulties",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="branchstatementmodel",
            name="others",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="branchstatementmodel",
            name="resources",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="goalmodel",
            name="given_help",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="goalmodel",
            name="indicator_action",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="subgoalmodel",
            name="given_help",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="subgoalmodel",
            name="indicator_action",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="subgoalmodel",
            name="parent_commitment",
            field=models.TextField(blank=True),
        ),
    ]
