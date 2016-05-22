from django.contrib import admin
from .models import *

class CelebAdmin(admin.ModelAdmin):
    search_fields = ['name']


# Register your models here.
admin.site.register(Celeb, CelebAdmin)
admin.site.register(TwitterAccount)
admin.site.register(FacebookAccount)
admin.site.register(InstagramAccount)
admin.site.register(Tweet)
admin.site.register(InstagramPost)
admin.site.register(FacebookPost)
