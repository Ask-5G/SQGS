from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from reports import views

urlpatterns = [
    url(r'^reports/$', views.ReportsView.as_view()),
    url(r'^reportdelivery/$', views.ReportDeliveryView.as_view()),
    url(r'^reportschedule/$', views.ReportScheduleView.as_view()),
    url(r'^ping/$', views.PingRequestView.as_view()),
    url(r'^image/(?P<pk>[0-9]+)/$', views.get_image),
    url(r'^images/$', views.ImagesView.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)