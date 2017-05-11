from django.contrib import admin
from .models import (
 					 Defects ,
  					 InspectionTypes,
  					 PartDefects,
   					 Repairs,
     				 Checkpoints,
     				 CheckpointDefects,
                     Checklist)
from organization.models import *
from basemodel.models import *
from modelclone import ClonableModelAdmin
from import_export import resources, fields

from import_export.widgets import *

from import_export.admin import ImportExportModelAdmin


class CheckpointsInline(admin.StackedInline):
    model = Checkpoints
    classes = ['collapse']
    extra = 0

class InspectionTypesAdmin(ClonableModelAdmin):
    inlines = CheckpointsInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)

class CheckpointDefectsInline(admin.StackedInline):
    model = CheckpointDefects
    classes = ['collapse']
    extra = 0

# class ModelStationResource(resources.ModelResource):
#     models = fields.Field(column_name='models', attribute='models', widget=ForeignKeyWidget(Models, 'description'))
#     stations = fields.Field(column_name='stations', attribute='stations', widget=ForeignKeyWidget(Stations, 'description'))
    
#     class Meta:
#         model = ModelStations
#         fields = ('id', 'models__description', 'stations__description')
#         export_order = ('id', 'models__description', 'stations__description')
#         skip_unchanged = True
#         report_skipped = True

#     def __unicode__(self):
#         return self.model.id

# class CheckpointsResource(resources.ModelResource):
#     inspectiontypes = fields.Field(column_name='inspectiontypes', attribute='inspectiontypes', widget=ForeignKeyWidget(InspectionTypes, 'description'))
#     modelstations = fields.Field(column_name='modelstations', attribute='modelstations', widget=ForeignKeyWidget(ModelStations, 'modelstations'))
#     parts = fields.Field(column_name='parts', attribute='parts', widget=ForeignKeyWidget(Parts, 'description'))

#     class Meta:
#         model = Checkpoints
#         fields = ('id', 'description', 'inspectiontypes__description', 'modelstations', 'parts__description')
#         export_order = ('id','description', 'inspectiontypes__description', 'modelstations', 'parts__description')
#         skip_unchanged = True
#         report_skipped = True

#     def __unicode__(self):
#         return self.model.id

# class CheckpointsAdmin(ClonableModelAdmin, ImportExportModelAdmin):
#     resource_class = CheckpointsResource
#     inlines = CheckpointDefectsInline,
#     clone_verbose_name = 'Clone it!'
  
#     list_display = ('description', 'inspectiontypes', 'modelstations', 'parts', 'is_new', 'clone_link',)
#     list_per_page = 10

#     search_fields = ('description',)

    # class Meta:
    #     model = Checkpoints

class PartDefectsInline(admin.StackedInline):
    model = PartDefects
    classes = ['collapse']
    extra = 0

class RepairsInline(admin.StackedInline):
    model = Repairs
    classes = ['collapse']
    extra = 0

class DefectsAdmin(ClonableModelAdmin):
    inlines = CheckpointDefectsInline, PartDefectsInline, RepairsInline,
    clone_verbose_name = 'Clone it!'
  
    list_display = ('description', 'defectcategories', 'sourcegates', 'clone_link',)
    list_per_page = 10

    search_fields = ('description',)   

class RepairsAdmin(ClonableModelAdmin):
    list_per_page = 10

admin.site.register(Defects, DefectsAdmin)
admin.site.register(InspectionTypes, InspectionTypesAdmin)
admin.site.register(PartDefects)
admin.site.register(Repairs, RepairsAdmin)
admin.site.register(Checkpoints)
admin.site.register(CheckpointDefects)
admin.site.register(Checklist)

