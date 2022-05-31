from django.contrib import admin

# Register your models here.
from .models import Consumption, Consumption_History, WaterPrice

admin.site.register(Consumption)
admin.site.register(Consumption_History)
admin.site.register(WaterPrice)