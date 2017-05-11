from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
import os
from django.utils import timezone
from web.settings import DEFAULT_KEY_VALIDITY_DURATION
import binascii
from basemodel.models import *
from reports.models import *

from PIL import Image
import time

class Plants(models.Model):
    
    plant_name = models.CharField(max_length=100)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Plant"
        db_table = 'Plants'
    
    def __str__(self):
        return self.plant_name 

signals.post_save.connect(save_updated_table, sender=Plants)        

class Cells(models.Model):
    
    description = models.CharField(max_length=300)
    plants = models.ForeignKey(Plants, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Cell"
        db_table = 'Cells'

    def __str__(self):
        return self.description

signals.post_save.connect(save_updated_table, sender=Cells)        


class Stations(models.Model):
    
    description = models.CharField(max_length=300)
    cells = models.ForeignKey(Cells, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)
    #order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Station"
        db_table = 'Stations'        

    def __str__(self):
        return self.description 

signals.post_save.connect(save_updated_table, sender=Stations)        

class ModelStations(models.Model):
    model = models.ForeignKey(Models, on_delete=models.CASCADE)  # Field name made lowercase.
    station = models.ForeignKey(Stations, on_delete=models.CASCADE)  # Field name made lowercase.
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Model Station"
        db_table = 'ModelStations'
        unique_together = (( 'model', 'station' ),)  
 
    def __unicode__(self):
        return ('%s-%s')%(self.model,self.station)

signals.post_save.connect(save_updated_table, sender=ModelStations)        


class Shifts(models.Model):
    description = models.CharField(max_length=300)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    plants = models.ForeignKey(Plants, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Shift"
        db_table = 'Shifts'

    def __str__(self):
        return self.description

signals.post_save.connect(save_updated_table, sender=Shifts)        




class Roles(models.Model):
    
    description = models.CharField(max_length=100)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Role"
        db_table = 'Roles'
 
    def __str__(self):
        return self.description 

signals.post_save.connect(save_updated_table, sender=Roles)        


class Users(models.Model):
   
    user_code = models.CharField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, default = "p@ssw0rd")
    mobile_number = models.IntegerField(null=True)
    email_id = models.CharField(max_length=200, null=True)
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True, editable=False, null=True)
    key_expiry_date = models.DateTimeField(blank=True, editable=False, null=True)
    is_updated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    designation = models.CharField(max_length=300, null=True)
    is_loggedin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        db_table = 'Users'

    def __str__(self):
        return self.name 

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def save(self, *args, **kwargs):
        if not self.key:
            self.generate_key()

        if not self.key_expiry_date:
            self.calculate_new_expiration()

        return super(Users, self).save(*args, **kwargs)

    def calculate_new_expiration(self):
        validity_duration = DEFAULT_KEY_VALIDITY_DURATION
        self.key_expiry_date = timezone.now() + validity_duration

    @property
    def is_expired(self):
        return self.key_expiry_date < timezone.now()

    def generate_key(self):
        self.key = binascii.hexlify(os.urandom(20)).decode()

signals.post_save.connect(save_updated_table, sender=Users)        

class SkillLevel(models.Model):
    description = models.CharField(max_length=60)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "SkillLevel"
        db_table = 'SkillLevel'

    def __str__(self):
        return ('%s')%(self.description)  

signals.post_save.connect(save_updated_table, sender=SkillLevel)        


class Stages(models.Model):
    
    description = models.CharField(max_length=300)
    stations = models.ForeignKey(Stations, on_delete=models.CASCADE)
    users = models.ManyToManyField(Users, through=u'StageUser',  related_name=u'stage_users')
    images = models.ForeignKey(Images, on_delete=models.CASCADE)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Stage"
        db_table = 'Stages'
    
    def __str__(self):
        return self.description 

signals.post_save.connect(save_updated_table, sender=Stages)      

class StageUser(models.Model):
    stages = models.ForeignKey(Stages, on_delete=models.CASCADE)
    users = models.ForeignKey(Users, on_delete=models.CASCADE) 
    shift = models.ForeignKey(Shifts, on_delete=models.CASCADE) 
    skill_level = models.ForeignKey(SkillLevel, on_delete=models.CASCADE) 
    last_modified_date = models.DateTimeField(auto_now=True, null=True)       
    
    def __unicode__(self):
        return ('%s')%(self.stages) 
        
signals.post_save.connect(save_updated_table, sender=StageUser)      


class UserLog(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    station = models.ForeignKey(Stations, on_delete=models.CASCADE, null=True)
    last_login = models.DateTimeField(auto_now=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "UserLog"
        db_table = 'UserLog'

    def __unicode__(self):
        return ('%s')%(self.user) 

class VerificationLog(models.Model):
    user_log = models.ForeignKey(UserLog, on_delete=models.CASCADE, null=True)
    stages = models.ForeignKey(Stages, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    is_skilled = models.BooleanField(default=True)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "VerificationLog"
        db_table = 'VerificationLog'

    def __unicode__(self):
        return ('%s')%(self.user_log) 

class DefectCategories(models.Model):
    description = models.CharField(max_length=60)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "DefectCategorie"
        db_table = 'DefectCategories'

    def __str__(self):
        return ('%s')%(self.description)

signals.post_save.connect(save_updated_table, sender=DefectCategories)      


class SourceGates(models.Model):
    description = models.CharField(max_length=60)
    last_modified_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "SourceGate"
        db_table = 'SourceGate'

    def __str__(self):
        return ('%s')%(self.description)
        
signals.post_save.connect(save_updated_table, sender=SourceGates)      

