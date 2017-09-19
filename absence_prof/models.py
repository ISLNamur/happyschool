from django.db import models


class MotifAbsence(models.Model):
    motif = models.CharField(max_length=200)

    def __str__(self):
        return self.motif


class Absence(models.Model):
    id_person = models.BigIntegerField(blank=True, null=True, default=None)
    name = models.CharField(max_length=500)
    motif = models.CharField(max_length=500)
    datetime_absence_start = models.DateTimeField("date du début de l'absence")
    datetime_absence_end = models.DateTimeField("date de la fin de l'absence")
    datetime_encoding = models.DateTimeField("date de l'encodage")
    comment = models.CharField(max_length=10000)
    user = models.CharField(max_length=20)

    class Meta:
        permissions = (
            ('access_absences', 'Can access to absences data'),
        )
