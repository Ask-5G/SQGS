from __future__ import unicode_literals
from django.db import models
from basemodel.models import *
from organization.models import *
from django.db.models import signals
from reports.models import *


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

class InspectionTypes(models.Model):
    
    description = models.CharField(max_length=300)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Inspection Type"
        db_table = 'InspectionTypes'
    
    def __str__(self):
        return self.description  

signals.post_save.connect(save_updated_table, sender=InspectionTypes)        

class Checkpoints(models.Model):

    description = models.CharField(max_length=45)
    inspectiontypes = models.ForeignKey(InspectionTypes, on_delete=models.CASCADE, db_column='InspectionTypes_id')  # Field name made lowercase.
    modelstations = models.ForeignKey(ModelStations, on_delete=models.CASCADE)
    parts = models.ForeignKey(Parts,on_delete=models.CASCADE)  # Field name made lowercase.
    is_new = models.BooleanField(default=False)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Checkpoint"
        db_table = 'Checkpoints'
        unique_together = (( 'description', 'inspectiontypes','parts','modelstations' ),)

    def __unicode__(self):
        return ('%s-%s-%s')%(self.description,self.inspectiontypes,self.parts)

signals.post_save.connect(save_updated_table, sender=Checkpoints)        

class Defects(models.Model):
  
    description = models.CharField(max_length=300)
    defectcategories = models.ForeignKey(DefectCategories, on_delete=models.CASCADE)
    sourcegates = models.ForeignKey(SourceGates, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Defect"
        db_table = 'Defects'
    
    def __unicode__(self):
        return ('%s-%s-%s')%(self.description,self.defectcategories,self.sourcegates)
        
signals.post_save.connect(save_updated_table, sender=Defects)        


class CheckpointDefects(models.Model):
   
    checkpoints = models.ForeignKey(Checkpoints, on_delete=models.CASCADE)  # Field name made lowercase.
    defects = models.ForeignKey(Defects, on_delete=models.CASCADE)  # Field name made lowercase.
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Checkpoint Defect"
        db_table = 'CheckpointDefects'

    def __unicode__(self):
        return ('%s-%s')%(self.checkpoints,self.defects)

signals.post_save.connect(save_updated_table, sender=CheckpointDefects)        

   
class PartDefects(models.Model):

    modelparts = models.ForeignKey(ModelParts, on_delete=models.CASCADE, null=True)
    defects = models.ForeignKey(Defects, on_delete=models.CASCADE)
    stages = models.ForeignKey(Stages, on_delete=models.CASCADE)  # Field name made lowercase.
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Part Defect"
        db_table = 'PartDefects'
        unique_together = (('modelparts', 'defects', 'stages'),)

    def __unicode__(self):
        return ('%s-%s-%s')%(self.modelparts,self.defects,self.stages)

signals.post_save.connect(save_updated_table, sender=PartDefects)        

   
class Repairs(models.Model):
    
    description = models.CharField(max_length=300)
    defects = models.ForeignKey(Defects, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Repair"
        db_table = 'Repairs'
        unique_together = (('defects', 'description'),)

    def __unicode__(self):
        return ('%s-%s')%(self.description,self.defects)
        
signals.post_save.connect(save_updated_table, sender=Repairs)        

class Checklist(models.Model):
    description = models.CharField(max_length=300, blank=True, null=True)
    repairs = models.ForeignKey(Repairs,null=True, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Checklist"
        db_table = 'Checklist'

    def __unicode__(self):
        return ('%s')%(self.description)
        
signals.post_save.connect(save_updated_table, sender=Checklist)        
