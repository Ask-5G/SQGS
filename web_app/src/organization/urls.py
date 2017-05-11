from django.conf.urls import url

from organization.views import DashboardView, ProductionView

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^production/$', ProductionView.as_view(), name='update'),
       
]