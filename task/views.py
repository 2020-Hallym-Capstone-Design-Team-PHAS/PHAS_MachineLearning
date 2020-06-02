from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from Test import *

def cf_task(request):
    filename = '/home/jovyan/work/capstone/명근심박_nr_v.wav'

    return HttpResponse(buat_prediction(filename))
