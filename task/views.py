from django.shortcuts import render
from hearbeat_cf import buat_prediction
# Create your views here.
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def cf_task(request):
    try:
        file_json = json.loads(request.body)
        filename = file_json['file_name']
        cf_data = buat_prediction(filename)

        return HttpResponse(json.dumps(cf_data))
    except Exception as e:
        return HttpResponse(e, " : Error 입니다.")
