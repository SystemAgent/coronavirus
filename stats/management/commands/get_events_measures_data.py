from collections import defaultdict
import requests, itertools, re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from _collections import defaultdict
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from psqlextra.query import ConflictAction


class Command(BaseCommand):
    help = 'Gets wikipedia data about Event and Measures by country for a specific month, ' \
           """February and March are available at present."""

    def add_arguments(self, parser):
        parser.add_argument('month', type=str)

    def handle(self, *args, **options):
        month = options['month']

        def get_wiki_events(month):
            res = requests.get(
                'https://en.wikipedia.org/wiki/Timeline_of_the_2019%E2%80%9320_coronavirus_pandemic_in_February_2020')
            res1 = requests.get(
                'https://en.wikipedia.org/wiki/Responses_to_the_2019%E2%80%9320_coronavirus_pandemic_in_March_2020')
            if month == 'February':
                wiki = BeautifulSoup(res.content, "lxml")
                first_h3 = wiki.find('h3')  # Start here
                uls = defaultdict(list)
                name = first_h3.text.strip()
                for sib in first_h3.find_next_siblings():
                    if sib.name == 'ul':
                        for event in sib.findAll("li"):
                            uls[name].append(event.text.strip())
                    elif sib.name == 'h3':
                        name = sib.text.strip()
                    elif sib.name == 'h2':
                        break
                    print(uls)
            elif month == 'March':
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
                    print(uls1)
        get_wiki_events(month)


#TODO Save scraped data to db
# for date, events in url.items():
#     for event in events:
#         (Total.objects
#             .on_conflict(['date', 'event'], ConflictAction.UPDATE)
#             .insert_and_get(date=date, event=event)
#         )
