from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
from datetime import datetime 
from .models import Total

def index(request):
    return HttpResponse("Coronavirus Project Bulgaria")


def graph(request):
    latest_totals = Total.objects.filter(country__startswith='Bulgaria').order_by('observation_date')
    js_data = {'date': [], 'deaths': [], 'recoveries': [], 'confirmed': []}
    for el in latest_totals:
        js_data['date'].append(str(el.observation_date))
        js_data['deaths'].append(el.deaths)
        js_data['recoveries'].append(el.recovered)
        js_data['confirmed'].append(el.confirmed)
    js_data = json.dumps(js_data)
    return render(request, 'graph/index.html', {'latest_totals': latest_totals[:5], 'js_data': js_data, 'fffa': 1})
  