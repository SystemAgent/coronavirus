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
            BASE_URL + 'time_series_covid19_confirmed_global.csv')
        deaths_df = pd.read_csv(
            BASE_URL + 'time_series_covid19_deaths_global.csv')
        recoveries_df = pd.read_csv(
            BASE_URL + 'time_series_covid19_recovered_global.csv')

        # preprocess
        def extract_data(df, type):
            country_df = df[df['Country/Region']==country]
            for index, row in country_df.iterrows():
                province = row['Province/State']
                for index, value in row.drop(['Province/State', 'Country/Region', 'Lat', 'Long']).items():
                    dt = pd.to_datetime(index)
                    new_total_arguments = {'observation_date': dt, 'country': country, 
                                            type: value, 'province_state': province}
                    (Total.objects
                        .on_conflict(['observation_date', 'country', 'province_state'], ConflictAction.UPDATE)
                        .insert_and_get(**new_total_arguments)
                    )

        extract_data(confirmed_df, 'confirmed')
        extract_data(deaths_df, 'deaths')
        extract_data(recoveries_df, 'recovered')

