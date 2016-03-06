# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Celeb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('twitter_id', models.CharField(max_length=20)),
                ('registered_time', models.DateTimeField(default=datetime.datetime(2016, 3, 6, 4, 5, 21, 380877, tzinfo=utc))),
                ('last_fetch_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('published_time', models.DateTimeField()),
                ('celeb', models.ForeignKey(related_name='tweets', to='celebs.Celeb')),
            ],
        ),
    ]
