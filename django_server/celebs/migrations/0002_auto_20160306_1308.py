# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('celebs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='celeb',
            name='last_fetch_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='celeb',
            name='registered_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 6, 4, 8, 51, 999124, tzinfo=utc)),
        ),
    ]
