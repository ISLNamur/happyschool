# Generated by Django 2.2.13 on 2020-07-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_auto_20200624_1753"),
    ]

    operations = [
        migrations.AddField(
            model_name="coresettingsmodel",
            name="student_teacher_relationship",
            field=models.CharField(
                choices=[("CL", "by classes"), ("CR", "by courses")],
                default="CL",
                help_text="Comment la relation entre les professeurs et les élèves est établie.",
                max_length=2,
            ),
        ),
    ]
