from django.db import models
from django.utils import timezone

from core.models import EmailModel, StudentModel


class Appel(models.Model):
    matricule = models.ForeignKey(StudentModel, on_delete=models.SET_NULL, to_field='matricule', null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    is_student = models.BooleanField(default=True)
    user = models.CharField(max_length=20, default="")
    objet = models.CharField(max_length=300)
    motif = models.CharField(max_length=300)
    datetime_motif_start = models.DateTimeField("Début date d'appel")
    datetime_motif_end = models.DateTimeField("Fin date d'appel")
    datetime_appel = models.DateTimeField("Date d'appel")
    commentaire = models.CharField(max_length=2000)
    traitement = models.CharField(max_length=2000, null=True, blank=True)
    datetime_traitement = models.DateTimeField("Date traitement", null=True, blank=True)
    is_traiter = models.BooleanField()
    emails = models.ManyToManyField(EmailModel, blank=True)
    custom_email = models.EmailField(default=None, blank=True, null=True)
    datetime_encodage = models.DateTimeField("Date d'encodage", default=timezone.now)

    class Meta:
        permissions = (
            ('access_appel', 'Can access to appel data'),
        )
