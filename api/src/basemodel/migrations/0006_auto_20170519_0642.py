# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-19 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basemodel', '0005_auto_20170512_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basemodels',
            options={'verbose_name': 'BaseModel'},
        ),
        migrations.AddField(
            model_name='modelparts',
            name='last_modified_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]