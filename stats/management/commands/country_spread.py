import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from psqlextra.query import ConflictAction

from stats.models import Total


class Command(BaseCommand):
    help = 'Gets hisorical coronavirus spread daa across a specific country'

    def add_arguments(self, parser):
        # named argument country
        # maybe add nargs to take an array of countries?
        parser.add_argument('country', type=str)

    def handle(self, *args, **options):
        country = options['country']

        # Base URL for coronavirus githubdata
        BASE_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
        confirmed_df = pd.read_csv(
            BASE_URL + 'time_series_19-covid-Confirmed.csv')
        deaths_df = pd.read_csv(BASE_URL + 'time_series_19-covid-Deaths.csv')
        recoveries_df = pd.read_csv(
            BASE_URL + 'time_series_19-covid-Recovered.csv')

        country_df = confirmed_df[confirmed_df['Country/Region'] == country]

        # preprocess
        final_df = pd.DataFrame()
        for df in [confirmed_df, deaths_df, recoveries_df]:
            country_df = df[df['Country/Region'] == country]
            country_df.drop(['Province/State', 'Country/Region',
                             'Lat', 'Long'], axis=1, inplace=True)
            country_df = country_df.T
            country_df.index = pd.to_datetime(country_df.index)
            final_df = pd.concat([final_df, country_df], axis=1)

        final_df.columns = ['confirmed', 'deaths', 'recoveries']

        def to_database(x):
            (Total.objects
                .on_conflict(['observation_date', 'country'], ConflictAction.UPDATE)
                .insert_and_get(observation_date=x.name, country=country, confirmed=x['confirmed'],
                                deaths=x['deaths'], recovered=x['recoveries'])
             )

        final_df.apply(lambda x: to_database(x), axis=1)
