from django.conf.urls import url

from reports.views import RftView, RftSearchView, RftRolldownModelView, RftRolldownStationView, DpuView, DpuSearchView, SummaryView, SummarySearchView, VinSummaryView, VinDetailsView,  RftFinalModelView, RftOverallModelView

urlpatterns = [
    url(r'^rft/$', RftView.as_view(), name='report'),
	url(r'^rft/search/$', RftSearchView.as_view(), name='rft_search'),
	url(r'^rft/rolldown/model/$', RftRolldownModelView.as_view(), name='rolldown_model'),	
	url(r'^rft/rolldown/station/$', RftRolldownStationView.as_view(), name='rolldown_station'),	
	url(r'^rft/final/model/$', RftFinalModelView.as_view(), name='final_model'),
	url(r'^rft/overall/model/$', RftOverallModelView.as_view(), name='overall_model'),	
	url(r'^dpu/$', DpuView.as_view(), name='report'), 
	url(r'^dpu/search/$', DpuSearchView.as_view(), name='dpu_search'),
	url(r'^summary/$', SummaryView.as_view(), name='summary'),
	url(r'^summary/search/$', SummarySearchView.as_view(), name='summary_search'),
	url(r'^summary/vin/$', VinSummaryView.as_view(), name='vin_summary'),
	url(r'^summary/vin_details/$', VinDetailsView.as_view(), name='vin_details'),
]