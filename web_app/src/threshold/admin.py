from django.contrib import admin
from models import Thresholds, ThresholdHistory, ThresholdNotifications

admin.site.register(Thresholds)
admin.site.register(ThresholdNotifications)
admin.site.register(ThresholdHistory)

