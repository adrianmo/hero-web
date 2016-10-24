from django.db import models


class NeutrinoAccount(models.Model):
    heroaccount = models.CharField(max_length=70)
    herousername = models.CharField(max_length=70)
    heropassword = models.CharField(max_length=70)
    used = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'heroneutrinoaccounts'


class Event(models.Model):
    event_text = models.TextField()
    event_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'worldevent'
