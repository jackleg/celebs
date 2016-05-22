#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import logging
import json
import sys
from datetime import datetime

import pytz

from util import import_django
import_django()

from django.utils import timezone
from celebs.models import InstagramAccount, InstagramPost

INSTAGRAM_CLIENT_ID="55f5c0abfc504f55b1579d7af3988e6a"

class InstagramDoc:
    def __init__(self):
        self.id           = ""
        self.thumbnail    = ""
        self.standard     = ""
        self.link         = ""
        self.created_time = ""
        self.caption      = ""
    
    def initialize(self):
        self.__init__()

    def __unicode__(self):
        return u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.created_time, self.link, self.thumbnail, self.standard, self.caption)

    def __str__(self):
        return unicode(self).encode("utf8")

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

def get_recent_posts(account):
    logging.info("get recent posts for %s" % account.id)
    RECENT_POST_BASE_URL = "https://api.instagram.com/v1/users/{0}/media/recent/".format(account.real_id)
    #https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN

    response = requests.get(RECENT_POST_BASE_URL, params={"client_id": INSTAGRAM_CLIENT_ID})

    if response.status_code != requests.codes.ok:
        logging.info("abnormal response code[{0}] for [{1}], {2}".format(response.status_code, account.id, response.url))
        return

    res_obj = json.loads(response.text)
    new_post_count = 0
    updated_post_count = 0
    for data in res_obj["data"]:
        instagram_model, created = InstagramPost.objects.update_or_create(
                                        defaults=dict(thumbnail=data["images"]["thumbnail"]["url"],
                                                      standard=data["images"]["standard_resolution"]["url"],
                                                      link=data["link"],
                                                      created_at=datetime.fromtimestamp(float(data["created_time"]), tz=pytz.UTC),
                                                      caption="" if data["caption"] is None else data["caption"]["text"],
                                                      comments_count=int(data['comments']['count']),
                                                      likes_count=int(data['likes']['count']),
                                                      last_fetch_time=timezone.now()),
                                        instagram_account=account,
                                        id=data["id"])
        if created: new_post_count += 1
        else: updated_post_count += 1

    account.last_fetch_time = timezone.now()
    account.save()

    logging.info("[%s] new post: %d, updated post: %d." % (account.id, new_post_count, updated_post_count))


if __name__=="__main__":
    #with open("sns.txt") as infile:
    #    for line in infile:
    #        data = line.rstrip("\n").split("\t")
    #        name          = data[0]
    #        instagram_url = data[4]

    #        if instagram_url == "": continue

    #        username = get_username_from_instagram_url(instagram_url)
    #        id       = get_userid_from_username(username)

    #        sys.stdout.write("{0}\t{1}\t{2}\n".format(name, username, id))    
    #for instagram_account in [InstagramAccount.objects.get(id='hongsick')]:
    for instagram_account in InstagramAccount.objects.all().order_by('-last_fetch_time'):
        logging.info("crawl instagram post for [%s]" % instagram_account.real_id)
 
        get_recent_posts(instagram_account)
