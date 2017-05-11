# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-26 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0009_remove_vinstatus_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vinstatus',
            options={'verbose_name': 'VinStatu'},
        ),
        migrations.AddField(
            model_name='vinstatus',
            name='latest_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
