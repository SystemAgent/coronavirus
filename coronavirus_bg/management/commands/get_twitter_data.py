import random
import pandas as pd
import tweepy
import requests
import json
from coronavirus_bg.models import Tweets
from psqlextra.query import ConflictAction
from coronavirus.settings import TWEEPY_TOKENS,USERNAMES

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Gets twitter data for a specific user, given a user_id and a tweet_id, used in since_id argument' \
           'to collect tweets since that one.'
    """Get all tweets (max 1000) for a new user."""

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=str)
        parser.add_argument('tweet_id', type= str)

    def handle(self, *args, **options):
        user_id = options['user_id']
        tweet_id = options['tweet_id']

        def make_tweepy_api():
            """Create a tweepy api with random tokens."""
            consumer_token, consumer_secret, access_token, access_token_secret = random.choice(
                TWEEPY_TOKENS)
            auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            return api

        def stitch(screen_name, tweets_id):
            base = 'https://twitter.com/{}/status/{}'.format(screen_name, tweets_id)
            return base

        api = make_tweepy_api()
        new_tweets = tweepy.Cursor(api.user_timeline, user_id=user_id, count=200, tweet_mode="extended",
                                   since_id=tweet_id, exclude_replies=True).items()
        print(new_tweets)
        results = [[tweet.user.id, tweet.id_str, tweet.created_at, tweet.full_text,
                    stitch(tweet.user.screen_name, tweet.id_str)] for tweet in new_tweets]
        print(results)
        if not results:
            return
        new_result = [{'user_id': el[0], 'tweet_id': el[1],
                      'datetime': el[2], 'text': el[3], 'url': el[4]} for el in results]
        final = pd.DataFrame(new_result)

        def dump(x):
            (Tweets.objects.on_conflict(['tweet_id', 'datetime'], ConflictAction.UPDATE)
                            .insert_and_get(user_id=x['user_id'], tweet_id=x['tweet_id'],
                                            datetime=x['datetime'],
                                            text=x['text'], url=x['url']))

        final.apply(lambda x: dump(x), axis=1)



# def get_newest_tweets(user_id, stop_slack_notifications=False):
#     """Get all new tweets for user we already have."""
#     api = make_tweepy_api()
#
#     new_tweets = tweepy.Cursor(api.user_timeline, user_id=user_id, tweet_mode="extended",
#                                since_id=latest, exclude_replies=True).items()
#     results = [[tweet.user.id, tweet.id, tweet.created_at,
#                 tweet.full_text, stitch(tweet.user.screen_name, tweet.id_str)] for tweet in new_tweets]
#     if not results:
#         return
#     new_result = [{'user_id': el[0], 'tweet_id': el[1],
#                    'datetime': el[2], 'text': el[3], 'url': el[4]} for el in results]





