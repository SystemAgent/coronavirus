import uuid

from django.db import models
from psqlextra.models import PostgresModel


class Total(PostgresModel):
    class Meta:
        unique_together = ('observation_date', 'country',)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observation_date = models.DateField('observation_date')
    country = models.CharField(max_length=1000)

    serial_number = models.IntegerField('serial_number', blank=True, null=True)
    province_state = models.CharField(max_length=1000, blank=True, null=True)
    last_update = models.DateTimeField('last_update', blank=True, null=True)
    confirmed = models.BigIntegerField(
        'confirmed_cases', blank=True, null=True)
    deaths = models.BigIntegerField('death_cases', blank=True, null=True)
    recovered = models.BigIntegerField(
        'recovered_cases', blank=True, null=True)


class Individual(PostgresModel):
    class Meta:
        unique_together = ('date_confirmation', 'country',)

    SEX_TYPES = (('M', 'Male'), ('F', 'Female'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField('country', max_length=1000)
    date_confirmation = models.DateField('date_confirmation')

    ID = models.IntegerField('identification_number', blank=True, null=True)
    age = models.IntegerField('age', blank=True, null=True)
    sex = models.CharField('sex', max_length=1,
                           choices=SEX_TYPES, blank=True, null=True)
    city = models.CharField('city', max_length=1000, blank=True, null=True)
    province = models.CharField(
        'province', max_length=1000, blank=True, null=True)
    date_onset = models.DateField('date_onset_symptoms', blank=True, null=True)
    date_admission = models.DateField(
        'date_admission_hospital', blank=True, null=True)
    symptoms = models.CharField(
        'symptoms', max_length=2000, blank=True, null=True)
    travel_dates = models.DateField(
        'travel_history_dates', blank=True, null=True)
    travel_location = models.CharField(
        'travel_history_location', max_length=1000, blank=True, null=True)


class Tweet(PostgresModel):
    class Meta:
        unique_together = ('tweet_id', 'datetime')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField('twitter_api_user_id', max_length=1000, blank=True, null=True)
    tweet_id = models.CharField('twitter_api_tweet_id', max_length=1000, blank=True, null=True)
    datetime = models.DateTimeField('twitter_api_datetime', blank=True, null=True)
    text = models.CharField('full_tweet_text', max_length=1000, blank=True, null=True)
    url = models.CharField('full_tweet_url', max_length=1000, blank=True, null=True)
    total_cases_bg = models.IntegerField('total_cases_infected_bulgaria', blank=True, null=True)
