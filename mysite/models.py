from django.db import models
from django.utils import timezone

# Create your models here.
class Consumption(models.Model):
    timelapse_in_min = models.FloatField()
    cubic_per_meter = models.FloatField()
    peso_per_cu_m = models.FloatField(default=0.5)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def to_standart_time(self):
        curr_datetime = timezone.localtime(self.date_created)
        return curr_datetime.strftime("%d/%m/%Y %I:%M:%S %p")

    def __str__(self):
        curr_datetime = timezone.localtime(self.date_created)
        return "{0}".format(curr_datetime.strftime("%d/%m/%Y %I:%M:%S %p"))


class Consumption_History(models.Model):
    timelapse_in_min = models.FloatField()
    cubic_per_meter = models.FloatField()
    peso_per_cu_m = models.FloatField(default=0.5)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def to_standart_time(self):
        curr_datetime = timezone.localtime(self.date_created)
        return curr_datetime.strftime("%d/%m/%Y %I:%M:%S %p")

    def __str__(self):
        curr_datetime = timezone.localtime(self.date_created)
        return "{0}".format(curr_datetime.strftime("%d/%m/%Y %H:%M:%S"))