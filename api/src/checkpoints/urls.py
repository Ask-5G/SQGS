from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from checkpoints import views

urlpatterns = [
    
    url(r'^defects/$', views.DefectsView.as_view()),
    url(r'^inspectiontypes/$', views.InspectionTypesView.as_view()),
    url(r'^partdefects/$', views.PartDefectsView.as_view()),
    url(r'^repairs/$', views.RepairsView.as_view()),
    url(r'^checkpoints/$', views.CheckpointsView.as_view()),
    url(r'^checkpointdefects/$', views.CheckpointDefectsView.as_view()),
    url(r'^checklist/$', views.ChecklistView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)