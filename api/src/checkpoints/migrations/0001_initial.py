# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-13 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basemodel', '0001_initial'),
        ('organization', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'Checklist',
                'verbose_name': 'Checklist',
            },
        ),
        migrations.CreateModel(
            name='CheckpointDefects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'CheckpointDefects',
                'verbose_name': 'Checkpoint Defect',
            },
        ),
        migrations.CreateModel(
            name='Checkpoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
                ('is_new', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Checkpoints',
                'verbose_name': 'Checkpoint',
            },
        ),
        migrations.CreateModel(
            name='Defects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('defectcategories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.DefectCategories')),
                ('sourcegates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.SourceGates')),
            ],
            options={
                'db_table': 'Defects',
                'verbose_name': 'Defect',
            },
        ),
        migrations.CreateModel(
            name='InspectionTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'InspectionTypes',
                'verbose_name': 'Inspection Type',
            },
        ),
        migrations.CreateModel(
            name='PartDefects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Defects')),
                ('modelparts', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basemodel.ModelParts')),
                ('stages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Stages')),
            ],
            options={
                'db_table': 'PartDefects',
                'verbose_name': 'Part Defect',
            },
        ),
        migrations.CreateModel(
            name='Repairs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('defects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Defects')),
            ],
            options={
                'db_table': 'Repairs',
                'verbose_name': 'Repair',
            },
        ),
        migrations.AddField(
            model_name='checkpoints',
            name='inspectiontypes',
            field=models.ForeignKey(db_column='InspectionTypes_id', on_delete=django.db.models.deletion.CASCADE, to='checkpoints.InspectionTypes'),
        ),
        migrations.AddField(
            model_name='checkpoints',
            name='modelstations',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.ModelStations'),
        ),
        migrations.AddField(
            model_name='checkpoints',
            name='parts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basemodel.Parts'),
        ),
        migrations.AddField(
            model_name='checkpointdefects',
            name='checkpoints',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Checkpoints'),
        ),
        migrations.AddField(
            model_name='checkpointdefects',
            name='defects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Defects'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='repairs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Repairs'),
        ),
        migrations.AlterUniqueTogether(
            name='repairs',
            unique_together=set([('defects', 'description')]),
        ),
        migrations.AlterUniqueTogether(
            name='partdefects',
            unique_together=set([('modelparts', 'defects', 'stages')]),
        ),
        migrations.AlterUniqueTogether(
            name='checkpoints',
            unique_together=set([('description', 'inspectiontypes', 'parts', 'modelstations')]),
        ),
    ]
