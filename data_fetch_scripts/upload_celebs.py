#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
celeb 정보들이 있는 sns.txt 파일을 parsing해서 django에서 사용중인 DB에 추가.
"""

import logging
import re
import sys

from util import import_django
import_django()

from celebs.models import Celeb, TwitterAccount, FacebookAccount, InstagramAccount
import instagram as ins_util


def get_id_from_url(url):
    """sns url에서 id 부분만 출력."""

    try:
        last_slash_index = url.rindex('/')
        return url[last_slash_index+1:]
    except ValueError:
        return ""
    

def make_sns_account(class_obj, id):

    if id == "": return None
    else:
        if class_obj.__name__ == "InstagramAccount":
            real_id = ins_util.get_userid_from_username(id)
            if real_id == None: return None
            
            class_obj.objects.get_or_create(id=id, defaults={"real_id": real_id})
        else:
            return class_obj.objects.get_or_create(id=id)[0]


logging.basicConfig(level=logging.INFO, format="[%(levelname)s][%(asctime)s] %(message)s")
category_pattern = re.compile(r" \((?P<category>.+)\)$") # 이름에 있는 카테고리명을 잡기 위함.

with open("sns.txt") as infile:
    created_count = 0
    updated_count = 0

    for line in infile:
        name, twitter, facebook, _, instagram, _ = line.rstrip("\n").split("\t")
        category = None
 
        category_match = category_pattern.search(name)
        if category_match:
            category = category_match.group('category')
            name = category_pattern.sub('', name)

        twitter_account = make_sns_account(TwitterAccount, get_id_from_url(twitter))
        facebook_account = make_sns_account(FacebookAccount, get_id_from_url(facebook))
        instagram_account = make_sns_account(InstagramAccount, get_id_from_url(instagram))

        celeb, created = Celeb.objects.update_or_create(
                                name=name, category=category,
                                defaults={'twitter_account': twitter_account,
                                          'facebook_account': facebook_account, 
                                          'instagram_account': instagram_account})

        if created:
            created_count += 1
            logging.info("created %s[%s]" % (name, category))
        else:
            updated_count += 1
            logging.info("updated %s[%s]" % (name, category))

