from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from basemodel.models import Models
from django.core.urlresolvers import reverse

class DashboardView(View):
    template_name = 'organization/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'username':'Guest User'})

class ProductionView(View):
    template_name = 'organization/top_tiles.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
            {'agco_models':Models.objects.filter(category__description="AGCO").count(),
            'hhp_models':Models.objects.filter(category__description="HHP").count(),
            'lhp_models':Models.objects.filter(category__description="LHP").count()}
            )
