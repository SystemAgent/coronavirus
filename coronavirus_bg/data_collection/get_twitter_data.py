import random
from django.conf import settings

settings.configure(DEBUG=True)
import pandas as pd
import spacy as sp
from spacy.symbols import number,NUM
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import tweepy
import requests
import json
from django.core.serializers.json import DjangoJSONEncoder
from coronavirus_bg.models import Tweets
from psqlextra.query import ConflictAction
from coronavirus.settings import TWEEPY_TOKENS,USERNAMES

def make_tweepy_api():
    """Create a tweepy api with random tokens."""
    consumer_token, consumer_secret, access_token, access_token_secret = random.choice(
        TWEEPY_TOKENS)
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def get_all_tweets(user_id):
    """Get all tweets (max 1000) for a new user."""
    api = make_tweepy_api()
    new_tweets = tweepy.Cursor(api.user_timeline, user_id=user_id, count=200, tweet_mode="extended",
                               since_id=1222977047670161408, exclude_replies=True).items()
    results = [[tweet.user.id, tweet.id_str, tweet.created_at, tweet.full_text,
                    stitch(tweet.user.screen_name, tweet.id_str)] for tweet in new_tweets]
    print(results)
    if not results:
        return
    new_result = [{'user_id': el[0], 'tweet_id': el[1],
                       'datetime': el[2], 'text': el[3], 'url': el[4]} for el in results]
    final = pd.DataFrame(new_result)
    # final.to_csv('./bg_tweets.csv', encoding='utf-8',index=True)
    # cases = final[final['text'].str.contains('COVID')]
    # print(cases['text'])

    # nlp = sp.load("en_core_web_sm")
    # matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
    # matcher.add("Cases", None, nlp('200 са'), nlp("100 е"))
    # doc = nlp(str(cases['text']))
    # matched = []
    # for match_id, start, end in matcher(doc):
    #     # print("Matched based on token shape:", doc[start:end])
    #     string_id = nlp.vocab.strings[match_id]
    #     span = doc[start:end]
    #     matched.append([token for token in span.subtree if token.like_num][0])
    #     print(span.text)
        # print(matched)
        # final['total_cases_bg'] =

    def dump(x):
        (Tweets.objects.on_conflict(['tweet_id', 'datetime'], ConflictAction.UPDATE)
                        .insert_and_get(user_id=final['user_id'], tweet_id=final['tweet_id'],
                                    datetime=final['datetime'],
                                    text=final['text'], url=final['url']))

    final.apply(lambda x: dump(x), axis=1)



# def get_newest_tweets(user_id, stop_slack_notifications=False):
#     """Get all new tweets for user we already have."""
#     api = make_tweepy_api()
#     url_tweet_id = BASE_URL + 'tweets/get_id?user_id={}'.format(user_id)
#     token = make_jwt_token(url_tweet_id)
#     r = requests.get(url_tweet_id, headers={'Authorization': token})
#
#     if r.status_code != 200:
#         if r.json()['error'] == 'There is no such user!':
#             return get_all_tweets(user_id)
#         else:
#             return
#     latest = r.json()['result']
#     new_tweets = tweepy.Cursor(api.user_timeline, user_id=user_id, tweet_mode="extended",
#                                since_id=latest, exclude_replies=True).items()
#     results = [[tweet.user.id, tweet.id, tweet.created_at,
#                 tweet.full_text, stitch(tweet.user.screen_name, tweet.id_str)] for tweet in new_tweets]
#     if not results:
#         return
#     new_result = [{'user_id': el[0], 'tweet_id': el[1],
#                    'datetime': el[2], 'text': el[3], 'url': el[4]} for el in results]
#     url_db = DATABASE_URL + 'tweets'
#     token = make_jwt_token(url_db)
#
#     try:
#         r = requests.post(url_db, data=json.dumps(new_result),
#                           headers={'Authorization': token, 'content-type': 'application/json'})


# def get_users_tweets(users):
#     stop_slack_notifications = False
#     for x in users:
#         get_newest_tweets(x, stop_slack_notifications)


def stitch(screen_name, tweet_id):
    base = 'https://twitter.com/{}/status/{}'.format(screen_name, tweet_id)
    return base


if __name__ == '__main__':
    get_all_tweets(3769353255)
