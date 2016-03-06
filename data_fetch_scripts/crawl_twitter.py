#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
import json

import requests

from util import import_django
import_django()

from celebs.models import Celeb, Tweet

TWITTER_BASE_URL='https://api.twitter.com/1.1/statuses/user_timeline.json'

ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJOttwAAAAAAeQpi6xxpixPcNVzpVokJnoVyuQg%3DuLLydn6vvdkkrJ9TFEOqli4etiHMfwojJPTgTc1BZNnrV47Pgl'
headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

for celeb in Celeb.objects.all():
	print celeb.name.encode('utf8')
	print celeb.twitter_id

	r = requests.get(TWITTER_BASE_URL, params={'screen_name': celeb.twitter_id}, headers=headers)
	for tweet in r.json():
		tweet_model, created = Tweet.objects.update_or_create(
									celeb=celeb,
									id=tweet['id'],
									text=tweet['text'],
									created_at=datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
									favorite_count=tweet['favorite_count'],
									retweet_count=tweet['retweet_count'])

		tweet_model.save()
		
		print "==="
		print tweet_model
		print created

