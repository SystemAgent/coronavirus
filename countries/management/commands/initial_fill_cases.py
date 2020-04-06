import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from countries.forms import CountryForm, DailyReportForm
from countries.models import DailyReport
from coronavirus import settings


COUNTRIES_FIXTURES = os.path.join(settings.BASE_DIR, 'countries', 'fixtures')


class Command(BaseCommand):
    help = "Initial fill of cases information"

    def handle(self, *args, **options):
        with open(os.path.join(COUNTRIES_FIXTURES, 'cases.csv')) as cases_file:
            with open(os.path.join(COUNTRIES_FIXTURES, 'deaths.csv')) as death_cases_file:
                with open(os.path.join(COUNTRIES_FIXTURES, 'recoveries.csv')) as recoveries_file:
                    cases_reader = csv.reader(cases_file, delimiter=',')
                    death_cases_reader = csv.reader(death_cases_file, delimiter=',')
                    recoveries_reader = csv.reader(recoveries_file, delimiter=',')
                    header = next(cases_reader)
                    next(death_cases_reader)
                    next(recoveries_reader)
                    errors = 0
                    for cases_row in cases_reader:
                        country = cases_row[1]
                        for index in range(4, len(cases_row)):
                            date = datetime.strptime(header[index], "%m/%d/%y")
                            cases = cases_row[index]
                            daily_report = DailyReport.objects.filter(country=country, date=date)
                            if len(daily_report) > 0:
                                daily_report = daily_report[0]
                                cases = int(cases) + daily_report.cases
                                form = DailyReportForm({'country': country, 'date': date, 'cases': cases, 'deaths': daily_report.deaths, 'recoveries': daily_report.recoveries}, instance=daily_report)
                                if form.is_valid():
                                    form.save()
                                else:
                                    print(country)
                                    errors += 1
                            else:
                                form = DailyReportForm({'country': country, 'date': date, 'cases': cases})
                                if form.is_valid():
                                    form.save()
                                else:
                                    print(country)
                                    errors += 1
                    print("Number of cases errors: {}".format(errors))

                    errors = 0
                    for death_cases_row in death_cases_reader:
                        country = death_cases_row[1]
                        for index in range(4, len(cases_row)):
                            date = datetime.strptime(header[index], "%m/%d/%y")
                            death_cases = death_cases_row[index]
                            daily_report = DailyReport.objects.filter(country=country, date=date)
                            if len(daily_report) > 0:
                                daily_report = daily_report[0]
                                death_cases = int(death_cases) + daily_report.deaths
                                form = DailyReportForm({'country': country, 'date': date, 'cases': daily_report.cases, 'deaths': death_cases, 'recoveries': daily_report.recoveries}, instance=daily_report)
                                if form.is_valid():
                                    form.save()
                                else:
                                    errors += 1
                            else:
                                form = DailyReportForm({'country': country, 'date': date, 'deaths': death_cases})
                                if form.is_valid():
                                    form.save()
                                else:
                                    errors += 1
                    print("Number of death cases errors: {}".format(errors))

                    errors = 0
                    for recoveries_row in recoveries_reader:
                        country = recoveries_row[1]
                        for index in range(4, len(cases_row)):
                            date = datetime.strptime(header[index], "%m/%d/%y")
                            recoveries = recoveries_row[index]
                            daily_report = DailyReport.objects.filter(country=country, date=date)
                            if len(daily_report) > 0:
                                daily_report = daily_report[0]
                                recoveries = int(recoveries) + daily_report.recoveries
                                form = DailyReportForm({'country': country, 'date': date, 'cases': daily_report.cases, 'deaths': daily_report.deaths, 'recoveries': recoveries}, instance=daily_report)
                                if form.is_valid():
                                    form.save()
                                else:
                                    errors += 1
                            else:
                                form = DailyReportForm({'country': country, 'date': date, 'recoveries': recoveries})
                                if form.is_valid():
                                    form.save()
                                else:
                                    errors += 1
                    print("Number of cases errors: {}".format(errors))
