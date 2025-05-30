# Generated by Django 4.2 on 2024-06-20 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_absence_teacher', '0016_alter_justificationmodel_absences'),
    ]

    operations = [
        migrations.CreateModel(
            name='JustMotiveModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=20, verbose_name='Short name')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
        ),
        migrations.AlterModelOptions(
            name='periodeducmodel',
            options={'ordering': ['start']},
        ),
        migrations.RemoveField(
            model_name='justificationmodel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='justificationmodel',
            name='short_name',
        ),
        migrations.AddField(
            model_name='justificationmodel',
            name='motive',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='student_absence_teacher.justmotivemodel'),
            preserve_default=False,
        ),
    ]
