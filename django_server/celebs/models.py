# -*- coding: utf8 -*-

from django.db import models
from django.utils import timezone

class Celeb(models.Model):
    """한 명의 Celeb을 저장하는 model."""
    name = models.CharField(max_length=100) # celeb의 이름
    category = models.CharField(max_length=50, null=True, blank=True) # celeb이 속하는 카테고리. 가수, 배우, etc.

    # each sns id.
    twitter_id = models.CharField(max_length=50, null=True, blank=True)
    facebook_id = models.CharField(max_length=50, null=True, blank=True)
    instagram_id = models.CharField(max_length=50, null=True, blank=True)

    registered_time = models.DateTimeField(default=timezone.now()) # 등록 시각.
    last_fetch_time = models.DateTimeField(null=True, blank=True) # 마지막으로 fetch한 시각.

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return u"{celeb.name} ({celeb.category})".format(celeb=self)

    def get_twitter_url(self):
        """twitter profile URL 반환"""
        if self.twitter_id:
            return "https://www.twitter.com/%s" % self.twitter_id
        else:
            return ""

    def get_facebook_url(self):
        """facebook profile URL 반환"""
        if self.facebook_id:
            return "https://www.facebook.com/%s" % self.facebook_id
        else:
            return ""

    def get_instagram_url(self):
        """instagram profile URL 반환"""
        if self.instagram_id:
            return "https://www.instagram.com/" % self.instagram_id
        else:
            return ""


class Tweet(models.Model):
    """하나의 tweet을 저장하기 위한 모델."""

    celeb = models.ForeignKey('celebs.Celeb', related_name='tweets') # 이 tweet을 쓴 사람
    id = models.BigIntegerField(primary_key=True) # tweet id
    text = models.TextField() # tweet 내용
    created_at = models.DateTimeField() # tweet을 작성한 시각
    favorite_count = models.IntegerField(default=0) # '좋아요' 수
    retweet_count = models.IntegerField(default=0) # 'RT' 수
    last_fetch_time = models.DateTimeField(default=timezone.now()) # 마지막 fetch time.

    def get_tweet_url(self):
        """이 tweet으로 바로 가기 위한 URL"""
        return "https://twitter.com/%s/status/%ld" % (self.celeb.twitter_id, self.id)

    def __unicode__(self):
        return unicode(self.text)
