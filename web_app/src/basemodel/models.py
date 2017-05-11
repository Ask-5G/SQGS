from __future__ import unicode_literals
from django.db import models
from django.db import IntegrityError
from django.db import models as django_models
from django.utils import timezone
import os
from django.db.models import signals
from reports.models import *
from PIL import Image
import time

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

class Parts(models.Model):   
    description = models.CharField(max_length=45)
    images = models.ForeignKey(Images, on_delete=models.CASCADE, null=True) 
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Part"
        db_table = 'Parts'  

    def __unicode__(self):
        return self.description 

signals.post_save.connect(save_updated_table, sender=Parts)        

class Market(models.Model):
    description = models.CharField(max_length=300, null=True)
    last_modified_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Market"
        db_table = 'Market'

    def __str__(self):
        return self.description

signals.post_save.connect(save_updated_table, sender=Market)    

class ModelCategory(models.Model):
    description = models.CharField(max_length=300, null=True)
    last_modified_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "ModelCategory"
        db_table = 'ModelCategory'

    def __str__(self):
        return self.description

signals.post_save.connect(save_updated_table, sender=ModelCategory)    

class Models(models.Model):
    base_sales_code = models.CharField(max_length=45, blank=True, null=True)
    sales_code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(ModelCategory, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(auto_now=True)
    last_modified_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Model"
        db_table = 'Models'

    def __str__(self):
        return self.description

signals.post_save.connect(save_updated_table, sender=Models)        

class ModelParts(models.Model):
    parts = models.ForeignKey(Parts,on_delete=models.CASCADE)  
    models = models.ForeignKey(Models, on_delete=models.CASCADE)  

    class Meta:
        verbose_name = "Model Part"
        db_table = 'ModelParts'
        unique_together = (('parts', 'models'),) 

    def __unicode__(self):
        return ('%s-%s')%(self.parts,self.models)

signals.post_save.connect(save_updated_table, sender=ModelParts)        







