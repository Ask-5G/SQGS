from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	url(r'^parts/', csrf_exempt(views.PartsView.as_view()), name= "parts"),
	url(r'^models/', csrf_exempt(views.ModelsView.as_view()), name= "models"),
	url(r'^modelparts/', csrf_exempt(views.ModelPartsView.as_view()), name= "modelparts"),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)