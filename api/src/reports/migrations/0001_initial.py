# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-13 11:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import reports.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_to', models.CharField(choices=[('Parts', 'Parts'), ('Stages', 'Stages'), ('InspectionDefects', 'InspectionDefects')], max_length=60)),
                ('description', models.CharField(max_length=60)),
                ('image', models.FileField(upload_to=reports.models.upload_image)),
            ],
            options={
                'db_table': 'Images',
                'verbose_name': 'Image',
            },
        ),
        migrations.CreateModel(
            name='ReportDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('role_id', models.IntegerField()),
            ],
            options={
                'db_table': 'ReportDelivery',
                'verbose_name': 'Report Delivery',
            },
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Reports',
                'verbose_name': 'Report',
            },
        ),
        migrations.CreateModel(
            name='ReportSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.CharField(max_length=45)),
                ('day', models.CharField(max_length=45)),
                ('month', models.CharField(max_length=45)),
                ('shift', models.CharField(max_length=45)),
                ('week', models.CharField(max_length=45)),
                ('reports', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Reports')),
            ],
            options={
                'db_table': 'ReportSchedule',
                'verbose_name': 'Report Schedule',
            },
        ),
        migrations.CreateModel(
            name='UpdatedTables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('priority', models.IntegerField(default=0)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'UpdatedTables',
            },
        ),
        migrations.AddField(
            model_name='reportdelivery',
            name='report_schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.ReportSchedule'),
        ),
        migrations.AlterUniqueTogether(
            name='reportschedule',
            unique_together=set([('id', 'reports')]),
        ),
        migrations.AlterUniqueTogether(
            name='reportdelivery',
            unique_together=set([('id', 'report_schedule')]),
        ),
    ]
