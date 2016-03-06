# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('celebs', '0002_auto_20160306_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='published_time',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='tweet',
            name='favorite_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweet',
            name='last_fetch_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 6, 10, 42, 16, 887135, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweet_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='celeb',
            name='last_fetch_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='celeb',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 6, 10, 42, 16, 886551, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
