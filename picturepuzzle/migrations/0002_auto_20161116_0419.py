# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picturepuzzle', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='puzzle',
        ),
        migrations.RemoveField(
            model_name='user_level',
            name='user',
        ),
        migrations.DeleteModel(
            name='user_level',
        ),
    ]
