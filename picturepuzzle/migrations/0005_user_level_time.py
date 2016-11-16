# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('picturepuzzle', '0004_auto_20161116_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_level',
            name='Time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
