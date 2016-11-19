# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('picturepuzzle', '0002_auto_20161116_0419'),
    ]

    operations = [
        migrations.CreateModel(
            name='puzzle',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('photo', models.ImageField(upload_to='/Pics')),
                ('solution', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='user_level',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('level', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
