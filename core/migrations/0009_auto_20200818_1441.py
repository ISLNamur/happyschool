# Generated by Django 2.2.13 on 2020-08-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_coresettingsmodel_student_teacher_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coresettingsmodel',
            name='student_teacher_relationship',
            field=models.CharField(choices=[('CL', 'by classes'), ('CR', 'by courses'), ('BO', 'by courses and by classes')], default='CL', help_text='Comment la relation entre les professeurs et les élèves est établie.', max_length=2),
        ),
    ]