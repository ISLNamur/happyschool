# Generated by Django 4.2 on 2024-07-01 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_absence_teacher', '0022_rename_student_responsible_warned_studentabsenceeducmodel_mail_warning'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailTemplateModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('template', models.TextField()),
            ],
        ),
    ]
