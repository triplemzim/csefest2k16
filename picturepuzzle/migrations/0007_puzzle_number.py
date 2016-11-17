# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picturepuzzle', '0006_user_level_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
