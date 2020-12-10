# Generated by Django 2.2.13 on 2020-12-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dossier_eleve', '0013_auto_20200512_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseleve',
            name='time_sanction_end',
            field=models.TimeField(blank=True, null=True, verbose_name='Heure de fin de la sanction'),
        ),
        migrations.AlterField(
            model_name='sanctiondecisiondisciplinaire',
            name='notify',
            field=models.ManyToManyField(blank=True, help_text="Permet d'envoyer une notification aux parents/responsable légal ou responsable de l'école\n            (éducateurs/coordonateur) à une fréquence particulière (tous les X fois).", to='dossier_eleve.NotifySanctionModel'),
        ),
    ]
