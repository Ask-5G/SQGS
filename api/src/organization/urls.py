from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from organization import views

urlpatterns = [
	url(r'^login/$', views.ObtainAuthToken.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
	url(r'^users/$', views.UsersView.as_view()),
	url(r'^roles/$', views.RolesView.as_view()),
	url(r'^plants/$', views.PlantsView.as_view()),
    url(r'^cells/$', views.CellsView.as_view()),
    url(r'^stations/$', views.StationsView.as_view()),
   	url(r'^modelstations/', views.ModelStationsView.as_view()), 
    url(r'^shifts/$', views.ShiftsView.as_view()),
    url(r'^stages/$', views.StagesView.as_view()),
    url(r'^userdeployment/$', views.VerificationLogView.as_view()),
    url(r'^skilllevel/$', views.SkilllevelView.as_view()),
    url(r'^stageuser/$', views.StageUserView.as_view()),
    url(r'^defectcategories/$', views.DefectCategoriesView.as_view()),
    url(r'^sourcegates/$', views.SourceGatesView.as_view()),


   ]

urlpatterns = format_suffix_patterns(urlpatterns)
