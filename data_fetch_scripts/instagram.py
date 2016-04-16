#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
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
