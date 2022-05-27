from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('historical_data', views.historical_data, name='historical_data'),
    path('paid', views.paid, name='paid'),
    path('api/add/consumption', views.add_consumption, name='add_consumption'),
    path('api/get/consumption', views.get_consumption, name='get_consumption'),
    path('api/get/history_consumption', views.get_history_consumption, name='get_history_consumption'),
]