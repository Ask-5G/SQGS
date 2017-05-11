# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basemodel', '0002_auto_20170426_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='last_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='modelcategory',
            name='last_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='models',
            name='last_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='parts',
            name='last_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
