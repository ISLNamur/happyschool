# Generated by Django 4.0.5 on 2022-11-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('student_absence_teacher', '0010_auto_20210915_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentabsenceteachersettingsmodel',
            name='can_see_adding',
            field=models.ManyToManyField(blank=True, default=None, related_name='can_see_adding', to='auth.group'),
        ),
    ]