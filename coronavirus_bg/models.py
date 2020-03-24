from django.db import models
import uuid
from psqlextra.models import PostgresModel

class Totals(models.Model):
    class Meta:
        db_table = 'totals'

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
    class Meta:
        db_table = 'individuals'

    SEX_TYPES = (('M', 'Male'), ('F', 'Female'),)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ID = models.IntegerField('identification_number')
    age = models.IntegerField('age')
    sex = models.CharField('sex', max_length=1, choices=SEX_TYPES)
    city = models.CharField('city', max_length=1000)
    province = models.CharField('province', max_length=1000)
    country = models.CharField('country', max_length=1000)
    date_onset = models.DateField('date_onset_symptoms')
    date_admission = models.DateField('date_admission_hospital')
    date_confirmation = models.DateField('date_confirmation')
    symptoms = models.CharField('symptoms', max_length=2000)
    travel_dates = models.DateField('travel_history_dates')
    travel_location = models.CharField(
        'travel_history_location', max_length=1000)


class Tweets(PostgresModel):
    class Meta:
        db_table = 'tweets'
        unique_together = ('tweet_id', 'datetime')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField('twitter_api_user_id', max_length=1000, blank=True, null=True)
    tweet_id = models.CharField('twitter_api_tweet_id', max_length=1000, blank=True, null=True)
    datetime = models.DateTimeField('twitter_api_datetime', blank=True, null=True)
    text = models.CharField('full_tweet_text', max_length=1000, blank=True, null=True)
    url = models.CharField('full_tweet_url', max_length=1000, blank=True, null=True)
    total_cases_bg = models.IntegerField('total_cases_infected_bulgaria', blank=True, null=True)
