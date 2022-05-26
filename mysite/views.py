from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


@csrf_exempt
def add_consumption(request):
    response_data = {}
    
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        print("at add_consumption: body: {0}".format(body))

        response_data['status_code'] = 200
        response_data['message'] = 'OK'
    else:
        response_data['status_code'] = 400
        response_data['message'] = "Bad Request"
    
    return JsonResponse(response_data)