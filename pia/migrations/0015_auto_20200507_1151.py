# Generated by Django 2.2.11 on 2020-05-07 09:51

from django.db import migrations, models
import django.db.models.deletion
import pia.models


class Migration(migrations.Migration):

    dependencies = [
        ('pia', '0014_auto_20200320_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=pia.models.unique_file_name)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProjectModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_project', models.TextField()),
                ('date_student_project', models.DateField()),
                ('datetime_creation', models.DateTimeField(auto_now_add=True)),
                ('datetime_update', models.DateTimeField(auto_now=True)),
                ('pia_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pia.PIAModel')),
            ],
        ),
        migrations.CreateModel(
            name='ParentsOpinionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parents_opinion', models.TextField()),
                ('date_parents_opinion', models.DateField()),
                ('datetime_creation', models.DateTimeField(auto_now_add=True)),
                ('datetime_update', models.DateTimeField(auto_now=True)),
                ('pia_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pia.PIAModel')),
            ],
        ),
        migrations.AddField(
            model_name='branchgoalmodel',
            name='attachments',
            field=models.ManyToManyField(blank=True, to='pia.AttachmentModel'),
        ),
        migrations.AddField(
            model_name='crossgoalmodel',
            name='attachments',
            field=models.ManyToManyField(blank=True, to='pia.AttachmentModel'),
        ),
    ]
