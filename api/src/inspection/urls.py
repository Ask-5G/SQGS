from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from inspection import views

urlpatterns = [
	url(r'^vindetails/$', views.VinDetailsView.as_view()),
    url(r'^inspectiondefects/$', views.InspectionDefectsView.as_view()),
    url(r'^defectclosure/$', views.DefectClosureView.as_view()),
    # url(r'^vin/close/$', views.VinstatusView.as_view()),
    #url(r'^calculationview/$', views.calculationview),
	url(r'^report/$', views.ReportView.as_view()),
	url(r'^final/$', views.FinalReportView.as_view()),

 
]

urlpatterns = format_suffix_patterns(urlpatterns)