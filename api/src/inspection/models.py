from __future__ import unicode_literals
from django.db import models
from checkpoints.models import *
from organization.models import *
from basemodel.models import *
from django.db.models import signals
from reports.models import *
from decimal import Decimal

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

def update_filename_inspectiondefects(instance, filename):
    path = 'images/inspectiondefects/'
    format = str(instance) +\
        "-" + str(timezone.now())
    return os.path.join(path,format)

def update_filename_defectclosure(instance, filename):
    path = 'images/defectclosure/'
    format = str(instance) +\
        "-" + str(timezone.now())
    return os.path.join(path,format)


class VinDetails(models.Model):
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    vin = models.CharField(max_length=45)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    stations = models.ForeignKey(Stations, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    closed_time = models.DateTimeField(auto_now_add=False, null=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE)
    vin_order = models.IntegerField()
    
    class Meta:
        verbose_name = "Vin Detail"
        db_table = 'VinDetails'
        unique_together = (( 'vin', 'stations'),)


    def __str__(self):
        return self.vin

signals.post_save.connect(save_updated_table, sender=VinDetails)        

class InspectionDefects(models.Model):
    vin = models.ForeignKey(VinDetails, on_delete=models.CASCADE)
    observations = models.CharField(max_length=300, null=True, blank=True)
    image_1 = models.ForeignKey(Images, on_delete=models.CASCADE, null=True, blank=True)
    image_2 = models.FileField(
        upload_to=update_filename_inspectiondefects,
        null=True, blank=True
    )
    image_quadrant = models.IntegerField(default=0, null=True, blank=True)
    created_time = models.DateTimeField(auto_now=False)
    updated_time = models.DateTimeField(auto_now=False)
    checkpoints = models.ForeignKey(Checkpoints, on_delete=models.CASCADE, null=True, blank=True)  # Field name made lowercase.
    partdefects = models.ForeignKey(PartDefects, on_delete=models.CASCADE, null=True, blank=True)  # Field name made lowercase.
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True,)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Inspection Defect"
        db_table = 'InspectionDefects'
        unique_together = (( 'vin', 'partdefects'),)

    def __str__(self):
        return str(self.observations)

signals.post_save.connect(save_updated_table, sender=InspectionDefects)        

class DefectClosure(models.Model):
    image_1 = models.FileField(
        upload_to=update_filename_defectclosure,
        null=True, blank=True
    )
    image_2 = models.CharField(max_length=45)
    image_quadrant = models.IntegerField(default=0, null=True, blank=True)
    created_time = models.DateTimeField(auto_now=False)
    updated_time = models.DateTimeField(auto_now=False)
    activity_id = models.IntegerField(default=0, null=True, blank=True)
    inspection_defects = models.ForeignKey(InspectionDefects, on_delete=models.CASCADE)
    repairs = models.ForeignKey(Repairs, on_delete=models.CASCADE)  
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True,)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Defect Closure"
        db_table = 'DefectClosure'
        unique_together = (('inspection_defects', 'repairs'),)

    def __unicode__(self):
        return ('%s')%(self.inspection_defects)

signals.post_save.connect(save_updated_table, sender=DefectClosure)   

class Verification(models.Model):
    vin = models.ForeignKey(VinDetails, on_delete=models.CASCADE, null=True)
    stations = models.ForeignKey(Stations, on_delete=models.CASCADE)
    defects_count = models.IntegerField(default=0, null=True, blank=True)
    closure_count = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=50, default='RFT NOT OK')
    timestamp = models.DateTimeField(auto_now_add=True, null=True) 
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Verification"
        db_table = 'Verification'

    def __unicode__(self):
        return ('%s')%(self.vin)

class VinStatus(models.Model):
   vin = models.CharField(max_length=300, null=True, blank=True)
   tot_defects = models.IntegerField(default=0, null=True, blank=True)
   tot_closure = models.IntegerField(default=0, null=True, blank=True)
   status = models.CharField(max_length=300, null=True, blank=True)
   last_modified_date = models.DateTimeField(auto_now_add=True, null=True)

   class Meta:
        verbose_name = "VinStatu"
        db_table = 'VinStatus'
        
   def __unicode__(self):
        return ('%s')%(self.vin)

class DefectsPerUnit(models.Model):
    no_of_defects = models.IntegerField(default=0, null=True, blank=True)
    no_of_tractors = models.IntegerField(default=0, null=True, blank=True)
    dpu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "DefectsPerUnit"
        db_table = 'DefectsPerUnit'
        
    def __unicode__(self):
        return ('%s')%(self.dpu)

class FinalRFT(models.Model):
    vin = models.CharField(max_length=300, null=True, blank=True)
    final_status = models.CharField(max_length=300, null=True, blank=True)
    overall_status = models.CharField(max_length=300, null=True, blank=True)
    last_modified_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "FinalRFT"
        db_table = 'FinalRFT'
        
    def __unicode__(self):
        return ('%s')%(self.vin)
