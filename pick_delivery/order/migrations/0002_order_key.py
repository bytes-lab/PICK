# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='key',
            field=models.CharField(default='fwf2fg3g3434534;', max_length=100),
            preserve_default=False,
        ),
    ]
