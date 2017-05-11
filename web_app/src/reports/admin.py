from django.contrib import admin
from models import Reports, ReportSchedule, ReportDelivery, Images

admin.site.register(Reports)
admin.site.register(ReportDelivery)
admin.site.register(ReportSchedule)
admin.site.register(Images)

