from django.shortcuts import render

import datetime

def index(request):
    now = datetime.datetime.now()
    newyear = now.month == 1 and now.day == 1
    return render(request, "newyear/index.html", {
        "newyear": newyear
    })
# Create your views here.
