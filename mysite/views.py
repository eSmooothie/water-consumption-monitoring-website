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

def historical_data(request):

    data = {}

    consumptions = Consumption_History.objects.all().order_by("-date_created")

    data['consumptions'] = consumptions

    return render(request, "mysite/historical_data.html", data)

def get_history_consumption(request):
    response_data = {}
    if request.method == 'GET':

        consumptions = Consumption_History.objects.all().order_by("-date_created")

        response_data["status_code"] = 200
        response_data["message"] = 'OK'

        data = []
        label = []

        for consumption in consumptions:
            dict_model = model_to_dict(consumption)
            data.append(dict_model)

        for consumption in consumptions:
            label.append(consumption.date_created)

        response_data["consumptions_data"] = data
        response_data["label"] = label

    else:
        response_data["status_code"] = 400
        response_data["message"] = 'Bad request'

    return JsonResponse(response_data)

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
        body_unicode = request.body

        print("at add_consumption: body_unicode: {0}".format(body_unicode))

        body = json.loads(body_unicode)

        print("at add_consumption: body: {0}".format(body))

        
        elapsed_time = body["elapsed_time"]
        elapsed_time = round(elapsed_time, 0)
        elapsed_time_in_min = convert_sec_to_min(elapsed_time)
        
        peso_per_cu_m = 0.24 #

        amount = elapsed_time_in_min['raw_min'] * peso_per_cu_m

        time_format = ""
        if elapsed_time_in_min['min'] != 0 and elapsed_time_in_min['sec'] != 0:
            time_format = "{0}m {1}s".format(elapsed_time_in_min['min'], elapsed_time_in_min['sec'])
        elif elapsed_time_in_min['min'] == 0:
            time_format = "{0}s".format(elapsed_time_in_min['sec'])
        elif elapsed_time_in_min['sec'] == 0:
            time_format = "{0}m".format(elapsed_time_in_min['min'])

        new_consumption = Consumption(
            timelapse_in_min = round(elapsed_time_in_min['raw_min'], 2),
            cubic_per_meter = round(elapsed_time_in_min['raw_min'], 2),
            timelapse_format = time_format,
            peso_per_cu_m = peso_per_cu_m,
            amount = round(amount,2)
        )

        new_consumption_hist = Consumption_History(
            timelapse_in_min = round(elapsed_time_in_min['raw_min'], 2),
            cubic_per_meter = round(elapsed_time_in_min['raw_min'], 2),
            timelapse_format = time_format,
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

def convert_sec_to_min(elapsed_time : float):
    raw_min = elapsed_time / 60
    min = elapsed_time // 60
    sec = elapsed_time - (min * 60)
    return {"min":min, "sec":sec, "raw_min": raw_min}