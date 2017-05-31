import base64

from django import forms
from django.contrib import admin
from .models import (Parts,
                     Models,
                     ModelParts,
                     Market,
                     ModelCategory,
                     BaseModels
                     )
from checkpoints.models import Checkpoints, PartDefects
from organization.models import ModelStations
from modelclone import ClonableModelAdmin
#from import_export import resources
from import_export import resources, fields

from import_export.widgets import *

from import_export.admin import ImportExportModelAdmin
from easy_select2 import select2_modelform

PartsForm = select2_modelform(Parts)

class ModelStationsInline(admin.StackedInline):
    model = ModelStations
    classes = ['collapse']
    extra = 0

class ModelPartsInline(admin.StackedInline):
    model = ModelParts
    classes = ['collapse']
    extra = 0

class CheckpointsInline(admin.StackedInline):
    model = Checkpoints
    classes = ['collapse']
    extra = 0

class PartDefectsInline(admin.StackedInline):
    model = PartDefects
    classes = ['collapse']
    extra = 0

class ModelAdmin(ClonableModelAdmin,ImportExportModelAdmin):
    inlines = ModelPartsInline, ModelStationsInline
    clone_verbose_name = 'Clone it!'
  
    list_display = ('sales_code', 'description', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

    class Meta:
        model = Models

class PartAdmin(ClonableModelAdmin, ImportExportModelAdmin):
    form = PartsForm        
    inlines = ModelPartsInline, CheckpointsInline
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description','images', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

    class Meta:
        model = Parts

class ModelPartsResource(resources.ModelResource):
    models = fields.Field(column_name='models', attribute='models', widget=ForeignKeyWidget(Models, 'description'))
    parts = fields.Field(column_name='parts', attribute='parts', widget=ForeignKeyWidget(Parts, 'description'))
    
    class Meta:
        model = ModelParts
        fields = ('id', 'models__description', 'parts__description')
        export_order = ('id', 'models__description', 'parts__description')
        skip_unchanged = True
        report_skipped = True

    def __unicode__(self):
        return self.model.id

class ModelPartsAdmin(ImportExportModelAdmin):
    inlines = PartDefectsInline,
    resource_class = ModelPartsResource

    list_per_page = 10
    # class Meta:
    #      model = ModelParts

admin.site.register(BaseModels)
admin.site.register(Models, ModelAdmin)
admin.site.register(Parts, PartAdmin)
admin.site.register(ModelParts, ModelPartsAdmin)
admin.site.register(Market)
admin.site.register(ModelCategory)


