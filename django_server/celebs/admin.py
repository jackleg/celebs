from django.contrib import admin
from .models import Celeb, TwitterAccount, FacebookAccount, InstagramAccount, Tweet, InstagramPost

# Register your models here.
admin.site.register(Celeb)
admin.site.register(TwitterAccount)
admin.site.register(FacebookAccount)
admin.site.register(InstagramAccount)
admin.site.register(Tweet)
admin.site.register(InstagramPost)