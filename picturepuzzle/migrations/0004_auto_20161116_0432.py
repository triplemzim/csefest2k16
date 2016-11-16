# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picturepuzzle', '0003_puzzle_user_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='photo',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='user_level',
            name='level',
            field=models.IntegerField(blank=True),
        ),
    ]
