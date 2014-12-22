#!/usr/bin/env python
# -*- coding: utf8 -*-

# todo
# 1. www.facebook.com/pages/ 처리
# 2. message가 없는 다른 상태에 대한 처리 (link 등은?)
# 3. message등의 데이터가 multiline인 경우 어떻게 하나?

import requests
import sys
import logging
import json

FACEBOOK_PREFIX="http://www.facebook.com/"
FACEBOOK_APP_ID="495992553876958"
FACEBOOK_APP_SECRET="93306d6ac05684c7c8543efd462b0668"
FACEBOOK_ACCESS_TOKEN=FACEBOOK_APP_ID+"|"+FACEBOOK_APP_SECRET

logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', level=logging.INFO)

def get_facebook_ids():
	result_dict         = {}
	facebook_prefix_len = len(FACEBOOK_PREFIX)

	with open("sns.txt", "r") as infile:
		logging.info("get facebook ids from %s" % infile.name)
		for line in infile:
			tokens = line.rstrip("\n").split("\t")
			name = tokens[0]
			facebook_url = tokens[2]
			if facebook_url == "": continue
			# todo: page는 어떻게 처리해야 할지 더 알아볼 것.			
			if facebook_url.startswith("http://www.facebook.com/pages/"): continue 
			facebook_id = facebook_url[facebook_prefix_len:]

			result_dict[name] = facebook_id
	
	logging.info("retrieve %d facebook ids." % len(result_dict))
	return result_dict

def get_facebook_post(userid):
	logging.info("get feed for [{0}]".format(userid))
	FEED_URL="https://graph.facebook.com/{0}/feed".format(userid)
	response = requests.get(FEED_URL, params={"access_token": FACEBOOK_ACCESS_TOKEN})
	if response.status_code != requests.codes.ok:
		logging.info("abnormal response code[{0}] for [{1}]".format(response.status_code, userid))
		return

	res_obj = json.loads(response.text)
	for post in res_obj['data']:
		try:
			id           = post['id'].encode('utf-8')
			created_time = post['created_time'].encode('utf-8')
			updated_time = post['updated_time'].encode('utf-8')
			message      = post['message'].encode('utf-8')	
			sys.stdout.write("{0}\t{1}\t{2}\t{3}\n".format(id, created_time, updated_time, message))
		except KeyError: # message가 없는 경우
			continue

facebook_ids = get_facebook_ids()
get_facebook_post(facebook_ids.values()[0])
