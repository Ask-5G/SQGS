from django.contrib import admin

from .models import InspectionDefects, DefectClosure, VinDetails, Verification, VinStatus, DefectsPerUnit, FinalRFT
from modelclone import ClonableModelAdmin
from import_export import resources, fields
from import_export.widgets import *

from import_export.admin import ImportExportModelAdmin

class VerificationAdmin(ClonableModelAdmin,ImportExportModelAdmin): 
    list_display = ('vin', 'stations', 'defects_count', 'closure_count', 'status',)
    list_per_page = 10

    search_fields = ('vin',)

    class Meta:
        model = Verification

class VinStatusAdmin(ClonableModelAdmin,ImportExportModelAdmin): 
    list_display = ('vin', 'tot_defects', 'tot_closure', 'status',)
    list_per_page = 10

    search_fields = ('vin',)

    class Meta:
        model = VinStatus

class DefectsPerUnitAdmin(ClonableModelAdmin,ImportExportModelAdmin): 
    list_display = ('no_of_defects', 'no_of_tractors', 'dpu', 'date')
    list_per_page = 10

    class Meta:
        model = DefectsPerUnit

admin.site.register(InspectionDefects)
admin.site.register(DefectClosure)
admin.site.register(VinDetails)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(VinStatus, VinStatusAdmin)
admin.site.register(DefectsPerUnit, DefectsPerUnitAdmin)
admin.site.register(FinalRFT)