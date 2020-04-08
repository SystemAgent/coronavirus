from django.forms import ModelForm
from countries.models import Country, DailyReport, Measure


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['name', 'population', 'first_case', 'first_death', 'emergency_state', 'quarantine']


class DailyReportForm(ModelForm):
    class Meta:
        model = DailyReport
        fields = ['date', 'country', 'cases', 'deaths', 'recoveries', 'critical']


class MeasureForm(ModelForm):
    class Meta:
        model = Measure
        fields = ['name', 'start_date', 'end_date', 'country']
