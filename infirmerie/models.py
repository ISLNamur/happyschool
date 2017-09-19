from django.db import models
from core.models import StudentModel


class Passage(models.Model):
    matricule = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, to_field='matricule', null=True, blank=True)
    name = models.CharField(max_length=100)
    datetime_arrive = models.DateTimeField("date d'arrivée")
    datetime_sortie = models.DateTimeField("date de sortie", null=True, blank=True)
    motifs_admission = models.CharField(max_length=2000)
    remarques_sortie = models.CharField(max_length=2000)

    class Meta:
        permissions = (
            ('access_infirmerie', 'Can access to infirmerie data'),
        )
