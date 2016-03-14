#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
import json
import logging
import time

import requests

from util import import_django
import_django()

from django.utils import timezone
from celebs.models import Celeb, Tweet


# to do. logging을 어떻게 할 것인지?
# to do. 이미 수집한 시점 이후의 tweets만 가져올 수 있나?
# to do. new가 계속 없는 사람, 혹은 response가 비정상인 사람은 제외해야 할 것 같은데.
# to do. error를 어느 선까지 처리해야 할까...?
TWITTER_BASE_URL='https://api.twitter.com/1.1/statuses/user_timeline.json'

ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJOttwAAAAAAeQpi6xxpixPcNVzpVokJnoVyuQg%3DuLLydn6vvdkkrJ9TFEOqli4etiHMfwojJPTgTc1BZNnrV47Pgl'
headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

logging.basicConfig(level=logging.INFO)

#r = requests.get(TWITTER_BASE_URL, params={'screen_name': "anwlrdlek"}, headers=headers)
#for tweet in r.json():
#   print json.dumps(tweet, indent=4)
for celeb in Celeb.objects.all().order_by('-last_fetch_time'):
    if celeb.twitter_id is None or celeb.twitter_id == "": continue

    logging.info("crawl tweets for [%s]" % celeb.name.encode('utf8'))
    new_tweet_count = 0
    updated_tweet_count = 0

    r = requests.get(TWITTER_BASE_URL, params={'screen_name': celeb.twitter_id}, headers=headers)

    # too many fetch. sleep and retry.
    while r.status_code == 429:
        time.sleep(10)
        r = requests.get(TWITTER_BASE_URL, params={'screen_name': celeb.twitter_id}, headers=headers)
    
    # 이런 경우 해당 celeb의 tweet을 제외해야 할 듯.
    if r.status_code != 200:
        logging.info('[%s][%d] does not open tweets.' % (celeb.name.encode('utf8'), r.status_code))
        continue

    for tweet_count, tweet in enumerate(r.json(), start=1):
        # celeb과 id로 tweet를 특정한 후, 새로 수집한 데이터로 업데이트한다.
        tweet_model, created = Tweet.objects.update_or_create(
                                    defaults=dict(text=tweet['text'],
                                                  created_at=datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
                                                  favorite_count=tweet['favorite_count'],
                                                  retweet_count=tweet['retweet_count']),
                                    celeb=celeb,
                                    id=tweet['id'])

        tweet_model.save()
        
        if created: new_tweet_count += 1
        else: updated_tweet_count += 1
    
    celeb.last_fetch_time = timezone.now()    
    celeb.save()

    logging.info("[%s] new tweet: %d, updated tweet: %d." % (celeb.name.encode('utf8'), new_tweet_count, updated_tweet_count))

    # tweet API가 15분마다 180 call로 제한.
    time.sleep(5)

logging.info("Done.")
