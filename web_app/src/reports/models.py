from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from PIL import Image
import time, os

from django.apps import apps

ordered_model_items = {
        "Images":1,
        "Plants": 2,
        "Cells": 3,
        "Stations":4,
        "Models":5,
        "ModelStations":6,
        "Stages":7,
        "Roles":8,
        "Users":9,
        "Shifts":10,
        "SkillLevel":11,
        "StageUser":12,
        "DefectCategories":13,
        "SourceGates":14,
        "Parts":15,
        "ModelParts":16,
        "InspectionTypes":17,
        "Checkpoints":18,
        "Defects":19,
        "CheckpointDefects":20,
        "Repairs":21,
        "Checklist":22,
        "PartDefects":23,
        "VinDetails":24,
        "InspectionDefects":25,
        "DefectClosure":26,
        "Market":27,
        "ModelCategory":28,
}

MODEL_CHOICES = (('Parts', 'Parts'),
                   ('Stages', 'Stages'),
                   ('InspectionDefects','InspectionDefects')
                   )

def save_updated_table(sender, instance, created, **kwargs):
    try:  
        update_tables = UpdatedTables.objects.get(
            name=instance.__class__.__name__
       )
        update_tables.save()
    except UpdatedTables.DoesNotExist:
        UpdatedTables.objects.create(
            name=instance.__class__.__name__,
            priority=ordered_model_items[instance.__class__.__name__]
        )

class Reports(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Report"
        db_table = 'Reports'

    def __str__(self):
        return self.name

signals.post_save.connect(save_updated_table, sender=Reports)        


class ReportSchedule(models.Model):
    
    hour = models.CharField(max_length=45)
    day = models.CharField(max_length=45)
    month = models.CharField(max_length=45)
    shift = models.CharField(max_length=45)
    week = models.CharField(max_length=45)
    reports = models.ForeignKey(Reports, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Report Schedule"
        db_table = 'ReportSchedule'
        unique_together = (('id', 'reports'),)

    def __str__(self):
        return self.week

signals.post_save.connect(save_updated_table, sender=ReportSchedule)                

class ReportDelivery(models.Model):
    
    user_id = models.IntegerField()
    role_id = models.IntegerField()
    report_schedule = models.ForeignKey(ReportSchedule, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Report Delivery"
        db_table = 'ReportDelivery'
        unique_together = (('id', 'report_schedule'),)

    def __str__(self):
        return self.report_schedule

signals.post_save.connect(save_updated_table, sender=ReportDelivery)                

class UpdatedTables(models.Model):
   
    name = models.CharField(max_length=60)
    priority = models.IntegerField(default=0)
    last_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UpdatedTables'

def resize(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    image.save(image_path, 'JPEG', quality=90)
    time.sleep(2)

def upload_image(instance, filename):
    path = 'images/'+instance.related_to
    format = str(instance.description) + '.jpg'
    return os.path.join(path, format)


class Images(models.Model):
    related_to = models.CharField(max_length=60,
            choices= MODEL_CHOICES
        )
    description = models.CharField(max_length=60)
    image = models.FileField(upload_to=upload_image)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)
    
    def save(self, *args, **kwargs):
        response = super(Images, self).save(*args, **kwargs)
        try:
            resize(self.image.path, 514, 411)
        except ValueError:
            pass
        return response

    class Meta:
        verbose_name = "Image"
        db_table = 'Images'

    def __str__(self):
        return ('%s-%s')%(self.related_to, self.description)
        
signals.post_save.connect(save_updated_table, sender=Images)                
