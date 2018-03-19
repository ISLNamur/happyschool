from django.db import models


class ScheduleChange(models.Model):
    date_start = models.DateField("Date de début")
    date_end = models.DateField("Date de fin", null=True, blank=True) # TODO Need (can be the same day)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    classes = models.CharField(default="", blank=True, max_length=100)
    activity = models.CharField(default="", blank=True, max_length=500)
    teachers = models.CharField(default="", blank=True, max_length=500)
    place = models.CharField(default="", blank=True, max_length=200)
    comment = models.CharField(default="", blank=True, max_length=500)
    datetime_encodage = models.DateTimeField("Date d'encodage")
    user = models.CharField(default="", blank=True, max_length=100)

    class Meta:
        ordering = ('date_start', 'time_start')
