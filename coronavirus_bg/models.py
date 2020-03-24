from django.db import models
from psqlextra.models import PostgresModel
import uuid


class Totals(PostgresModel):
    class Meta:
        db_table = 'totals'
        unique_together = ('observation_date', 'country',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_date = models.DateField('observation_date')
    country = models.CharField(max_length=1000)

    serial_number = models.IntegerField('serial_number', blank=True, null=True)
    province_state = models.CharField(max_length=1000, blank=True, null=True)
    last_update = models.DateTimeField('last_update', blank=True, null=True)
    confirmed = models.BigIntegerField('confirmed_cases', blank=True, null=True)
    deaths = models.BigIntegerField('death_cases', blank=True, null=True)
    recovered = models.BigIntegerField('recovered_cases', blank=True, null=True)


class Individuals(PostgresModel):
    class Meta:
        db_table = 'individuals'
        unique_together = ('date_confirmation', 'country',)

    SEX_TYPES = (('M', 'Male'), ('F', 'Female'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField('country', max_length=1000)
    date_confirmation = models.DateField('date_confirmation')

    ID = models.IntegerField('identification_number', blank=True, null=True)
    age = models.IntegerField('age', blank=True, null=True)
    sex = models.CharField('sex', max_length=1, choices=SEX_TYPES, blank=True, null=True)
    city = models.CharField('city', max_length=1000, blank=True, null=True)
    province = models.CharField('province', max_length=1000, blank=True, null=True)
    date_onset = models.DateField('date_onset_symptoms', blank=True, null=True)
    date_admission = models.DateField('date_admission_hospital', blank=True, null=True)
    symptoms = models.CharField('symptoms', max_length=2000, blank=True, null=True)
    travel_dates = models.DateField('travel_history_dates', blank=True, null=True)
    travel_location = models.CharField(
        'travel_history_location', max_length=1000, blank=True, null=True)
