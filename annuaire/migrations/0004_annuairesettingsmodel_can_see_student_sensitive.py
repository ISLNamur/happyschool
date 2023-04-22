# Generated by Django 2.2.11 on 2020-05-12 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("annuaire", "0003_auto_20200501_1806"),
    ]

    operations = [
        migrations.AddField(
            model_name="annuairesettingsmodel",
            name="can_see_student_sensitive",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                help_text="Permet aux groupes sélectionnés de voir les données sensibles de l'étudiant comme son\n            adresse, date de naissance, etc.",
                related_name="can_see_student_sensitive",
                to="auth.Group",
            ),
        ),
    ]
