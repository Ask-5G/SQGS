from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from threshold import views

urlpatterns = [
    url(r'^thresholds/$', views.ThresholdsView.as_view()),
    url(r'^thresholdnotification/$', views.ThresholdNotificationView.as_view()),
    url(r'^thresholdhistory/$', views.ThresholdHistoryView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)