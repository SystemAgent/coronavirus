from django.http import Http404
from django.shortcuts import render

from .models import Country, DailyReport


def countries_list(request):
    countries = Country.objects.all()
    return render(request, 'countries/countries.html', {'countries': countries})


def country_cases(request, country):
    try:
        country = Country.objects.get(name=country)
        cases = DailyReport.objects.filter(country=country).order_by('date')
    except:
        raise Http404("Country does not exist")
    return render(request, 'countries/cases_by_country.html', {'cases': cases})
    
