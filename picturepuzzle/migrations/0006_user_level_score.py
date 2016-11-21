# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picturepuzzle', '0005_user_level_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_level',
            name='score',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
