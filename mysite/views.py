from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.forms.models import model_to_dict

from .models import Consumption, Consumption_History

import json
# Create your views here.
def index(request):

    consumptions = Consumption.objects.all().order_by("-date_created")

    total_amount = 0.00
    if consumptions:
        total_amount = Consumption.objects.aggregate(total_amount=Sum('amount'))['total_amount']

    data = {
        'consumptions': consumptions,
        'total_amount': round(total_amount,2),
        }
    return render(request, 'mysite/index.html', data)

def get_consumption(request):
    response_data = {}
    if request.method == 'GET':

        consumptions = Consumption.objects.all().order_by("-date_created")

        response_data["status_code"] = 200
        response_data["message"] = 'OK'

        raw_data = []

        for consumption in consumptions:
            dict_model = model_to_dict(consumption)
            dict_model["created_at"] = str(consumption)
            raw_data.append(dict_model)

        response_data["consumptions_data"] = raw_data

        if consumptions:
            total_amount = Consumption.objects.aggregate(total_amount=Sum('amount'))['total_amount'] 
            response_data["total_amount"] = round(total_amount, 2)
        else:
            response_data["total_amount"] = "0.0"

    else:
        response_data["status_code"] = 400
        response_data["message"] = 'Bad request'

    return JsonResponse(response_data)

def paid(request):
    Consumption.objects.all().delete()
    
    return redirect('index')


@csrf_exempt
def add_consumption(request):
    response_data = {}
    
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print("at add_consumption: body: {0}".format(body))

        
        elapsed_time = body["elapsed_time"]
        elapsed_time_in_min = convert_sec_to_min(elapsed_time)

        amount = elapsed_time_in_min * 0.5

        peso_per_cu_m = 0.5

        new_consumption = Consumption(
            timelapse_in_min = round(elapsed_time_in_min,2),
            cubic_per_meter = round(elapsed_time_in_min,2),
            peso_per_cu_m = peso_per_cu_m,
            amount = round(amount,2)
        )

        new_consumption_hist = Consumption_History(
            timelapse_in_min = round(elapsed_time_in_min,2),
            cubic_per_meter = round(elapsed_time_in_min,2),
            peso_per_cu_m = peso_per_cu_m,
            amount = round(amount,2)
        )
        
        new_consumption.save()
        new_consumption_hist.save()

        response_data['status_code'] = 200
        response_data['message'] = 'OK'

    else:
        response_data['status_code'] = 400
        response_data['message'] = "Bad Request"
    
    return JsonResponse(response_data)

def convert_sec_to_min(sec : float):
    return sec / 60