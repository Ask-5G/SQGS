from django.conf.urls import url

from reports.views import * 

urlpatterns = [
    url(r'^rft/$', RftView.as_view(), name='report'),
	url(r'^rft/search/$', RftSearchView.as_view(), name='rft_search'),
	url(r'^rft/filter$', RftFilterView.as_view(), name='rft_filter'),
	url(r'^rft/rolldown/view/$', RftRolldownView.as_view(), name='rft_rolldown_view'),
	url(r'^rft/final/view/$', RftFinalView.as_view(), name='rft_final_view'),
	url(r'^rft/overall/view/$', RftOverallView.as_view(), name='rft_overall_view'),
	url(r'^dpu/$', DpuView.as_view(), name='report'), 
	url(r'^dpu/filter/$', DpuFilterView.as_view(), name='dpu_filter'),
	url(r'^dpu/rolldown/view/$', DpuRolldownView.as_view(), name='dpu_rolldown_view'),
	url(r'^dpu/final/view/$', DpuFinalView.as_view(), name='dpu_final_view'),
	url(r'^dpu/overall/view/$', DpuOverallView.as_view(), name='dpu_overall_view'),	 	 
	url(r'^dpu/search/$', DpuSearchView.as_view(), name='dpu_search'),
	url(r'^summary/$', SummaryView.as_view(), name='summary'),
	url(r'^summary/search/$', SummarySearchView.as_view(), name='summary_search'),
	url(r'^summary/vin/$', VinSummaryView.as_view(), name='vin_summary'),
	url(r'^summary/vin_details/$', VinDetailsView.as_view(), name='vin_details'),
]