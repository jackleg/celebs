#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import logging
import json
import sys

INSTAGRAM_CLIENT_ID="55f5c0abfc504f55b1579d7af3988e6a"

logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', level=logging.INFO)

# username(e.g. taeyeon_ss)에서 userid(e.g. 329452045)를 얻는 함수.
def get_userid_from_username(username):
	SEARCH_USER_BASE_URL = "https://api.instagram.com/v1/users/search"
	response = requests.get(SEARCH_USER_BASE_URL, params={"client_id": INSTAGRAM_CLIENT_ID, "q": username})
	if response.status_code != requests.codes.ok:
		logging.info("abnormal response code[{0}] for [{1}]".format(response.status_code, username))
		return

	res_obj = json.loads(response.text)
	for user in res_obj["data"]:
		if user["username"] == username:
			return user["id"]

# instagram url(e.g. http://www.instagram.com/PATRYGUILLAUME)에서 username 부분만 추출하는 함수
# "/"로 구분되는 가장 마지막 필드를 사용.
def get_username_from_instagram_url(instagram_url):
	return instagram_url.rsplit("/", 1)[-1]

if __name__=="__main__":
	with open("sns.txt") as infile:
		for line in infile:
			data = line.rstrip("\n").split("\t")
			name          = data[0]
			instagram_url = data[4]

			if instagram_url == "": continue

			username = get_username_from_instagram_url(instagram_url)
			id       = get_userid_from_username(username)

			sys.stdout.write("{0}\t{1}\t{2}\n".format(name, username, id))	
