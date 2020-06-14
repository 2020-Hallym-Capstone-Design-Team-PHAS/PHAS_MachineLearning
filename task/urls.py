
from django.urls import path
from task.views import *

urlpatterns = [
                path("heartbeat", cf_task, name = "cf_task"),
              ]
