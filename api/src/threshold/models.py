from __future__ import unicode_literals

from django.db import models
from django.db.models import signals


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

class Thresholds(models.Model):
    
    name = models.CharField(max_length=100)
    no_of_occurances = models.CharField(max_length=100)
    duration = models.CharField(max_length=45)
    reset_upon_notification = models.CharField(max_length=45)
    inspection_point_defects = models.IntegerField()

    class Meta:
        verbose_name = "Threshold"
        db_table = 'Thresholds'
    
    def __str__(self):
        return self.name

signals.post_save.connect(save_updated_table, sender=Thresholds)                
 
class ThresholdHistory(models.Model):
    
    timestamp = models.DateTimeField(blank=True, null=True)
    threshold = models.ForeignKey(Thresholds, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Threshold History"
        db_table = 'ThresholdHistory'


    def __str__(self):
        return self.timestamp

signals.post_save.connect(save_updated_table, sender=ThresholdHistory)                

     
class ThresholdNotifications(models.Model):
    
    role_id = models.IntegerField()
    user_id = models.IntegerField()
    threshold = models.ForeignKey(Thresholds, null=True, on_delete=models.CASCADE )

    class Meta:
        verbose_name = "Threshold Notification"
        db_table = 'ThresholdNotifications'

    def __str__(self):
        return self.role_id

signals.post_save.connect(save_updated_table, sender=ThresholdNotifications)                


