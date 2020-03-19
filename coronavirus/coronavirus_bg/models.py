from django.db import models
import uuid


class Totals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.IntegerField('serial_number')
    observation_date = models.DateField('observation_date')
    province_state = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)
    last_update = models.DateTimeField('last_update')
    confirmed = models.BigIntegerField('confirmed_cases')
    deaths = models.BigIntegerField('death_cases')
    recovered = models.BigIntegerField('recovered_cases')


class Individuals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ID = models.IntegerField('identification_number')
    age = models.IntegerField('age')
    sex = models.CharField('sex', max_length=100)
    city = models.CharField('city', max_length=1000)
    province = models.CharField('province', max_length=1000)
    country = models.CharField('country', max_length=1000)
    date_onset = models.DateField('date_onset_symptoms')
    date_admission = models.DateField('date_admission_hospital')
    date_confirmation = models.DateField('date_confirmation')
    symptoms = models.CharField('symptoms', max_length=2000)
    travel_dates = models.DateField('travel_history_dates')
    travel_location = models.CharField('travel_history_location', max_length=1000)

