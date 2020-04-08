import requests, itertools, re
from bs4 import BeautifulSoup
import numpy as np
from _collections import defaultdict
import pandas as pd
from django.core.management.base import BaseCommand, CommandError


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
                new = pd.DataFrame(df['measures'].str.split("]', ").tolist(), index=df.date).stack()
                new = new.reset_index([0, 'date'])
                new.columns = ['date', 'measures']
                dfs.append(new)
                print(dfs)
            df_result = pd.concat(dfs)
            return df_result

        def get_wiki_events(month):
            if month == 'February':
                get_february()
            elif month == 'March':
                get_march()
            elif month == 'all':
                frames = []
                febs = get_february()
                march = get_march()
                frames.append(febs)
                frames.append(march)
                # print(frames[1])
                print(parse_concat(frames))

        get_wiki_events(month)


#TODO Save scraped data to db
# for date, events in url.items():
#     for event in events:
#         (Total.objects
#             .on_conflict(['date', 'event'], ConflictAction.UPDATE)
#             .insert_and_get(date=date, event=event)
#         )
