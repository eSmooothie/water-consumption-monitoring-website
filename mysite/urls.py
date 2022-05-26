from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/add/consumption', views.add_consumption, name='add_consumption'),
]