from django.db import models

# Create your models here.
class Consumption(models.Model):
    timelapse_in_min = models.IntegerField()
    cubic_per_meter = models.FloatField()
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)


class Consumption_History(models.Model):
    timelapse_in_min = models.IntegerField()
    cubic_per_meter = models.FloatField()
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)