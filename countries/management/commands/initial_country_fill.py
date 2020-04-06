import csv
import os

from django.core.management.base import BaseCommand, CommandError

from countries.forms import CountryForm
from coronavirus import settings


COUNTRIES_FIXTURES = os.path.join(settings.BASE_DIR, 'countries', 'fixtures')


class Command(BaseCommand):
    help = "Initial fill of the country information"

    def handle(self, *args, **options):
        with open(os.path.join(COUNTRIES_FIXTURES, 'countries_population.csv')) as country_file:
            country_reader = csv.reader(country_file, delimiter=';')
            header = next(country_reader)
            errors = 0
            rows = 0
            for row in country_reader:
                rows += 1
                form = CountryForm({'name': row[0], 'population': row[2]})
                if form.is_valid():
                    form.save()
                else:
                    errors += 1
            print("Result: {}/{}".format(rows - errors, rows))
