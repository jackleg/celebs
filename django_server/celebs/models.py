# -*- coding: utf8 -*-

from django.db import models
from django.utils import timezone

class Celeb(models.Model):
    """한 명의 Celeb을 저장하는 model."""
    name = models.CharField(max_length=100) # celeb의 이름
    category = models.CharField(max_length=50, null=True, blank=True) # celeb이 속하는 카테고리. 가수, 배우, etc.
    registered_time = models.DateTimeField(default=timezone.now()) # 등록 시각.

    # each sns account
    # many-to-one relation.
    twitter_account = models.ForeignKey('TwitterAccount', related_name='celebs', on_delete=models.SET_NULL, null=True, blank=True)
    facebook_account = models.ForeignKey('FacebookAccount', related_name='celebs', on_delete=models.SET_NULL, null=True, blank=True)
    instagram_account = models.ForeignKey('InstagramAccount', related_name='celebs', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return u"{celeb.name} ({celeb.category})".format(celeb=self)


class SnsAccount(models.Model):
    """Sns Account를 나타내기 위한 클래스.

    아직 sub class에서 추가되는 필드는 없지만
    실제 ID와 URL을 반환하기 위한 모습은 다를 수 있고
    SNS마다 테이블을 따로 만들어야 하므로 abstract class로 구현한다"""

    id = models.CharField(max_length=50, primary_key=True)
    registered_time = models.DateTimeField(default=timezone.now()) # 등록 시각.
    last_fetch_time = models.DateTimeField(null=True, blank=True) # 마지막으로 fetch한 시각.

    def get_account_url(self):
        raise NotImplementedError

    class Meta:
        abstract = True


class TwitterAccount(SnsAccount):
    def get_account_url(self):
        return "https://www.twitter.com/%s" % self.id

    def __unicode__(self):
        return u"[twitter] %s" % self.id


class FacebookAccount(SnsAccount):
    def get_account_url(self):
        return "https://www.facebook.com/%s" % self.id

    def __unicode__(self):
        return u"[facebook] %s" % self.id


class InstagramAccount(SnsAccount):
    def get_account_url(self):
        return "https://www.instagram.com/" % self.id

    def __unicode__(self):
        return u"[instagram] %s" % self.id


class Tweet(models.Model):
    """하나의 tweet을 저장하기 위한 모델."""

    twitter_account = models.ForeignKey('TwitterAccount', related_name='tweets', on_delete=models.CASCADE) # 이 tweet을 account

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
        return u"[{self.id}] {self.text}".format(self=self)
