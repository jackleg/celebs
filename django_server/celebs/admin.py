from django.contrib import admin
from .models import Celeb, Tweet

# Register your models here.
admin.site.register(Celeb)
admin.site.register(Tweet)