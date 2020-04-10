import requests, itertools, re
from bs4 import BeautifulSoup
from _collections import defaultdict
from datetime import datetime
import pandas as pd
import spacy
import os
from django.core.management.base import BaseCommand, CommandError
from countries.forms import MeasureForm
from coronavirus import settings

COUNTRIES_FIXTURES = os.path.join(settings.BASE_DIR, 'countries', 'fixtures')


class Command(BaseCommand):
    help = 'Gets WiKipedia data about Event and Measures by country for a specific month, ' \
           """February and March are available at present."""

    def add_arguments(self, parser):
        parser.add_argument('month', type=str)

    def handle(self, *args, **options):
        month = options['month']

        def get_february():
            res = requests.get(
                'https://en.wikipedia.org/wiki/Timeline_of_the_2019%E2%80%9320_coronavirus_pandemic_in_February_2020')
            wiki = BeautifulSoup(res.content, "lxml")
            first_h3 = wiki.find(
                attrs={'class': "mw-headline", 'id': "Reactions_and_measures_outside_mainland_China"})
            uls = defaultdict(list)
            name = first_h3.text.strip()
            for sib in first_h3.find_all_next():
                if sib.name == 'p':
                    uls[name].append(sib.text.strip())
                if sib.name == 'h3':
                    name = sib.text.strip()
                elif sib.name == 'h2':
                    break
            df1 = pd.DataFrame(list(uls.items()), columns=['date', 'measures'])
            return df1

        def get_march():
            res1 = requests.get(
                'https://en.wikipedia.org/wiki/Responses_to_the_2019%E2%80%9320_coronavirus_pandemic_in_March_2020')
            wiki1 = BeautifulSoup(res1.content, "lxml")
            second_h3 = wiki1.find(attrs={'class': "mw-headline", 'id': "1_March"})
            uls1 = defaultdict(list)
            name1 = second_h3.text.strip()
            for sib in second_h3.find_all_next():
                if sib.name == 'p':
                    uls1[name1].append(sib.text.strip())
                if sib.name == 'h3':
                    name1 = sib.text.strip()
                elif sib.name == 'h2':
                    break
            df2 = pd.DataFrame(list(uls1.items()), columns=['date', 'measures'])
            return df2

        def parse_concat(list_dfs):
            dfs = []
            for df in list_dfs:
                new = pd.DataFrame([(tup.date, measure) for tup in df.itertuples() for measure in tup.measures])
                new.columns = ['date', 'measures']
                dfs.append(new)
            df_result = pd.concat(dfs)
            return df_result

        def get_wiki_events(month):
            if month == 'February':
                return get_february()
            elif month == 'March':
                return get_march()
            elif month == 'all':
                frames = []
                feb = get_february()
                march = get_march()
                frames.append(feb)
                frames.append(march)
                #Get final dataframe and clean up dates and measures columns
                all_data = parse_concat(frames)
                all_data['date'] = all_data['date'].str.replace('[[edit][edit][edit][edit]]', '2020', regex=True)
                all_data['date'] = all_data['date'].str.replace('[', ',', regex=True)
                all_data['date'] = pd.to_datetime(all_data['date'], errors='coerce')
                all_data['measures'] = all_data['measures'].str.replace('[[0-9][0-9]]', ' ', regex=True)
                all_data = all_data.dropna()

                # extract entities for country field
                sp = spacy.load("en_core_web_sm")
                countries = []
                countries_population = os.path.join(COUNTRIES_FIXTURES, 'countries_population.csv')
                csv = pd.read_csv(countries_population, delimiter=';')
                options = set(csv['name'].values)
                for text in all_data['measures'].tolist():
                    doc = sp(text)
                    for ent in doc.ents:
                        if ent.label_ == 'GPE':
                            if ent.text in options:
                                countries.append(ent.text)
                            all_data['countries'] = pd.Series(countries[:444])

                return all_data

        final = get_wiki_events(month)
        errors = 0
        rows = 0

        for row in final.itertuples(index=True):
            rows += 1
            form = MeasureForm({'name': getattr(row, "measures"), 'start_date': getattr(row, "date"),
                                'end_date': getattr(row, "date"), 'country': getattr(row, 'countries')})
            if form.is_valid():
                form.save()
            else:
                errors += 1
        print("Result: {}/{}".format(rows - errors, rows))
