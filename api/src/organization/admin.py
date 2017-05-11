import base64

from django import forms
from django.contrib import admin
from .models import *
from checkpoints.models import Checkpoints, PartDefects
from modelclone import ClonableModelAdmin

class CheckpointsInline(admin.StackedInline):
    model = Checkpoints
    classes = ['collapse']
    extra = 0

class ModelStationsAdmin(ClonableModelAdmin):
    inlines = CheckpointsInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('model', 'station', 'clone_link',)
    list_per_page = 10

    search_fields = ('model',)

class PartDefectsInline(admin.StackedInline):
    model = PartDefects
    classes = ['collapse']
    extra = 0

class StageUserInline(admin.StackedInline):
    model = StageUser
    classes = ['collapse']
    extra = 0

class StagesAdmin(ClonableModelAdmin):
    inlines = StageUserInline, PartDefectsInline, 
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description', 'stations', 'images', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

class CellsInline(admin.StackedInline):
    model = Cells
    classes = ['collapse']
    extra = 0

class ShiftsInline(admin.StackedInline):
    model = Shifts
    classes = ['collapse']
    extra = 0

class PlantsAdmin(ClonableModelAdmin):
    inlines = CellsInline, ShiftsInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('plant_name', 'clone_link',)
    list_per_page = 10

    search_fields = ('plant_name',)

class StationsInline(admin.StackedInline):
    model = Stations
    classes = ['collapse']
    extra = 0

class CellsAdmin(ClonableModelAdmin):
    inlines = StationsInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description', 'plants', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

class ModelStationsInline(admin.StackedInline):
    model = ModelStations
    classes = ['collapse']
    extra = 0

class StagesInline(admin.StackedInline):
    model = Stages
    classes = ['collapse']
    extra = 0

class RolesInline(admin.StackedInline):
    model = Roles
    classes = ['collapse']
    extra = 0

class StationsAdmin(ClonableModelAdmin):
    inlines = ModelStationsInline, StagesInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description', 'cells', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

class UsersAdmin(ClonableModelAdmin):
    #inlines = RolesInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('user_code', 'name', 'clone_link',)
    list_per_page = 10

    search_fields = ('name',)

class VerificationLogAdmin(ClonableModelAdmin): 
    list_display = ('user_log', 'stages', 'user', 'is_skilled')
    list_per_page = 10

    search_fields = ('user_log',)

admin.site.register(Stages)
admin.site.register(StageUser)
admin.site.register(Plants, PlantsAdmin)
admin.site.register(Cells, CellsAdmin)
admin.site.register(Stations, StationsAdmin)
admin.site.register(ModelStations, ModelStationsAdmin)
admin.site.register(Shifts)
admin.site.register(Roles)
admin.site.register(Users, UsersAdmin)
admin.site.register(UserLog)
admin.site.register(VerificationLog, VerificationLogAdmin)
admin.site.register(DefectCategories)
admin.site.register(SourceGates)
admin.site.register(SkillLevel)