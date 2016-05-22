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
from datetime import datetime
from dateutil.parser import parse

import pytz

from util import import_django
import_django()

from django.utils import timezone
from celebs.models import FacebookAccount, FacebookPost

FACEBOOK_PREFIX="http://www.facebook.com/"
FACEBOOK_APP_ID="495992553876958"
FACEBOOK_APP_SECRET="93306d6ac05684c7c8543efd462b0668"
FACEBOOK_ACCESS_TOKEN=FACEBOOK_APP_ID+"|"+FACEBOOK_APP_SECRET


logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', level=logging.INFO)


def get_likes_count(object_id):
    logging.info("get likes count for [%s]" % object_id)
    LIKES_URL = "https://graph.facebook.com/%s/likes" % object_id
    response = requests.get(LIKES_URL, params={"summary": "true", "access_token": FACEBOOK_ACCESS_TOKEN})

    try:
        likes_count = response.json()["summary"]["total_count"]
    except:
        likes_count = 0

    return likes_count


def get_comments_count(object_id):
    logging.info("get comments count for [%s]" % object_id)
    LIKES_URL = "https://graph.facebook.com/%s/comments" % object_id
    response = requests.get(LIKES_URL, params={"summary": "true", "access_token": FACEBOOK_ACCESS_TOKEN})

    try:
        comments_count = response.json()["summary"]["total_count"]
    except:
        comments_count = 0

    return comments_count


def get_recent_posts(fa):
    logging.info("get feed for [{0}]".format(fa.id))

    FEED_URL="https://graph.facebook.com/{0}/feed".format(fa.id)
    response = requests.get(FEED_URL, params={"access_token": FACEBOOK_ACCESS_TOKEN})
    if response.status_code != requests.codes.ok:
        logging.info("abnormal response code[{0}] for [{1}]".format(response.status_code, userid))
        return

    new_post_count = 0
    updated_post_count = 0
    try:
        for data in response.json()["data"]:
            # 본인이 직접 쓴 글이 아니면 skip.
            if data["from"]["id"] != fa.real_id: continue

            id = data["id"]
            object_id = data.get("object_id", None)
            shares_count = data["shares"]["count"] if "shares" in data else 0 
            defaults = dict(message=data.get("message", None),
                            picture=data.get("picture", None),
                            source=data.get("source", None),
                            link=data.get("link", None),
                            created_at=parse(data["created_time"]),
                            shares_count=shares_count,
                            likes_count=get_likes_count(id),
                            comments_count=get_comments_count(id))

            fp_model, created = FacebookPost.objects.update_or_create(
                                        defaults=defaults,
                                        object_id=object_id,
                                        facebook_account=fa,
                                        id=id)

            if created: new_post_count += 1
            else: updated_post_count += 1

        fa.last_fetch_time = timezone.now()
        fa.save()    

        logging.info("[%s] new post: %d, updated post: %d." % (fa.id, new_post_count, updated_post_count))
    except KeyError as e:
        logging.info("[%s] has no data. please check." % fa.id)


def get_real_id(fa):
    if fa.real_id is not None and fa.real_id != "0": return

    logging.info("get real id for [%s]" % fa.id)

    USER_URL = "https://graph.facebook.com/%s" % fa.id
    response = requests.get(USER_URL, params={'access_token': FACEBOOK_ACCESS_TOKEN})

    if response.status_code == requests.codes.ok:
        fa.real_id = response.json()["id"]
        fa.save()
        return True
    elif response.status_code == requests.codes.not_found:
        logging.info("[%s] is personal page (not allowed) or not exists." % fa.id)
        return False
    else:
        raise RuntimeError("abnormal response code[%d] for [%s], check [%s]" % (response.status_code, fa.id, response.url))


 
if __name__ == '__main__':
    for facebook_account in FacebookAccount.objects.all().order_by('-last_fetch_time'):
        logging.info("crawl facebook post for [%s]" % facebook_account.id)
        if get_real_id(facebook_account):
            get_recent_posts(facebook_account) 
