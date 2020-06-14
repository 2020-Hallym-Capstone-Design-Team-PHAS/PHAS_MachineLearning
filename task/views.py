from django.shortcuts import render
from hearbeat_cf import HeartbeatCF
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

def cf_task(request):
    try:
        h = HeartbeatCF()
        filename = request.GET.get('file_name')
        cf_data = HeartbeatCF.buat_prediction(h, filename)
        return HttpResponse('u')
    except Exception as e:
        return e
