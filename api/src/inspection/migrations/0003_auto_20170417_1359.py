# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-17 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0002_verification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verification',
            options={'verbose_name': 'Verification'},
        ),
        migrations.AlterModelTable(
            name='verification',
            table='Verification',
        ),
    ]
