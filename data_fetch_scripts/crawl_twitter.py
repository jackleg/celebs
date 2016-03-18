#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
import json
import logging
import time

import requests
from dateutil import parser

from util import import_django
import_django()

from django.utils import timezone
from celebs.models import TwitterAccount, Tweet


# to do. logging을 어떻게 할 것인지?
# to do. 이미 수집한 시점 이후의 tweets만 가져올 수 있나?
# to do. new가 계속 없는 사람, 혹은 response가 비정상인 사람은 제외해야 할 것 같은데.
# to do. error를 어느 선까지 처리해야 할까...?
TWITTER_BASE_URL='https://api.twitter.com/1.1/statuses/user_timeline.json'

ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJOttwAAAAAAeQpi6xxpixPcNVzpVokJnoVyuQg%3DuLLydn6vvdkkrJ9TFEOqli4etiHMfwojJPTgTc1BZNnrV47Pgl'
headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

logging.basicConfig(level=logging.INFO, format='[%(levelname)s][%(asctime)s] %(message)s')

#r = requests.get(TWITTER_BASE_URL, params={'screen_name': "anwlrdlek"}, headers=headers)
#for tweet in r.json():
#   print json.dumps(tweet, indent=4)
#for twitter_account in [TwitterAccount.objects.get(id='jackleg83')]:
for twitter_account in TwitterAccount.objects.all().order_by('-last_fetch_time'):
    logging.info("crawl tweets for [%s]" % twitter_account.id)
    new_tweet_count = 0
    updated_tweet_count = 0

    r = requests.get(TWITTER_BASE_URL, params={'screen_name': twitter_account.id}, headers=headers)

    # too many fetch. sleep and retry.
    while r.status_code == 429:
        time.sleep(10)
        r = requests.get(TWITTER_BASE_URL, params={'screen_name': twitter_account.id}, headers=headers)
    
    # 이런 경우 해당 celeb의 tweet을 제외해야 할 듯.
    if r.status_code != 200:
        logging.info('[%s][%d] does not open tweets.' % (twitter_account.id, r.status_code))
        continue

    for tweet_count, tweet in enumerate(r.json(), start=1):
        # celeb과 id로 tweet를 특정한 후, 새로 수집한 데이터로 업데이트한다.
        tweet_model, created = Tweet.objects.update_or_create(
                                    defaults=dict(text=tweet['text'],
                                                  created_at=parser.parse(tweet['created_at']),
                                                  favorite_count=tweet['favorite_count'],
                                                  retweet_count=tweet['retweet_count']),
                                    twitter_account=twitter_account,
                                    id=tweet['id'])

        if created: new_tweet_count += 1
        else: updated_tweet_count += 1
    
    twitter_account.last_fetch_time = timezone.now()    
    twitter_account.save()

    logging.info("[%s] new tweet: %d, updated tweet: %d." % (twitter_account.id, new_tweet_count, updated_tweet_count))

    # tweet API가 15분마다 180 call로 제한.
    time.sleep(5)

logging.info("Done.")
