#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
twitter에서 tweets를 수집하기 위해서는 application level의 token이 필요하다.
이것을 bearer token이라 칭하는데,
이것을 얻기 위한 application-only authorization 과정을 구현한다.
참고: https://dev.twitter.com/oauth/application-only
'''

import urllib
import base64
import requests

# todo: 이런 설정들을 config file로 이동시키는 것이 좋을 듯.
consumer_key = 'n5mAGfPqcJF8MHLUSDC5oMeao'
consumer_secret = 'VCQ8wQIMzUhppDRKIxQHlnciD5mOzML232BIWT3w5gjhFwq86v'

# 1. consumer key와 secret을 urlencoding한다.
# 이 전후로 key와 secret값이 변하지는 않지만, 미래에 바뀔 것을 대비해서 과정을 수행한다.
url_encoded_consumer_key = urllib.quote(consumer_key)
url_encoded_consumer_secret = urllib.quote(consumer_secret)

# 2. base64 encoded key를 구한다.
b64encoded = base64.b64encode(url_encoded_consumer_key + ":" + url_encoded_consumer_secret)

# 3. 아래와 같은 header와 body 설정으로 post request를 던진다.
post_headers = {
    'Authorization': 'Basic ' + b64encoded,
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
r = requests.post('https://api.twitter.com/oauth2/token', headers=post_headers, data='grant_type=client_credentials')

# 4. request가 성공한다면 아래와 같이 token_type이 bearer로, access_token이 넘어온다.
json_obj = r.json()
if json_obj['token_type'] == u'bearer':
	access_token = json_obj['access_token']
else:
	raise ValueError('Authorization failed!')

print "=== get token ==="
print access_token

# 5. 성공하면 다음부터는 아래와 같이 get으로 API를 콜 할 때, header에 Authorization 필드를 추가한다.
r = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=locogocrazy&count=5',
		headers={'Authorization': 'Bearer ' + access_token})

for tweet in r.json():
	print tweet['text'].encode('utf8')
