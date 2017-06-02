from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from basemodel.models import Models
from organization.models import * 
from inspection.models import VinStatus, VinDetails, Verification, DefectsPerUnit, FinalRFT, InspectionDefects, DefectClosure
from checkpoints.models import * 
from datetime import date, datetime, timedelta as td
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .forms import *
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from dateutil.parser import parse
from reports.templatetags import custom_tags
from collections import defaultdict
from collections import Counter
from itertools import chain


def get_user_dict(request):
    return {
        "user": 'Guest User',
        "plant": ''
        }

class Common(object):

    def parse_date(self, date):
        return datetime.strptime(date, '%d-%m-%Y %H:%M:%S').date()

    def get_date_list(self, from_date, to_date):
        _date_list = []
        delta = to_date - from_date
        for i in range(delta.days + 1):
            _date = from_date + td(days=i)
            _date_list.append(_date.strftime('%d-%m-%Y'))
        return _date_list

    def get_vin_details(self,user):
        if user['plant'] != '':
            return VinDetails.objects.filter(stations__in=Stations.objects.filter(cells__plants=user['plant']))
        else:
            return VinDetails.objects.all()



class RftView(TemplateView):
    common = Common()
    template_name = 'reports/rft.html'

    def get_context_data(self, **kwargs):
        user = get_user_dict(self.request)
        context = super(RftView, self).get_context_data(**kwargs)
        rolldown_filter_form = RftRolldownFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        final_filter_form = RftFinalFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        overall_filter_form = RftOverallFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        context = {
            'username': user['user'],
            'rolldown_filter_form': rolldown_filter_form,
            'final_filter_form': final_filter_form,
            'overall_filter_form': overall_filter_form
        }
        return context
	
class RftFilterView(View):

    def post(self, request):
        if 'rft_rolldown_plants' in request.POST:
            rolldown_form = RftRolldownFilterForm(user=get_user_dict(request), initial=request.POST)
            rolldown_filter_form = self.render_to_rft_rolldown_template(request, rolldown_form)
            return JsonResponse(rolldown_filter_form, safe=False)
        if 'rft_final_plants' in request.POST:
            final_form = RftFinalFilterForm(user=get_user_dict(request), initial=request.POST)
            final_filter_form = self.render_to_rft_final_template(request, final_form)
            return JsonResponse(final_filter_form, safe=False)
        if 'rft_overall_plants' in request.POST:
            overall_form = RftOverallFilterForm(user=get_user_dict(request), initial=request.POST)
            overall_filter_form = self.render_to_rft_overall_template(request, overall_form)
            return JsonResponse(overall_filter_form, safe=False)

    def render_to_rft_rolldown_template(self, request, form):
        template = TemplateResponse(request, 'reports/rft_rolldown_filter_form.html', {
            'rolldown_filter_form': form,
        })
        template.render()
        return template.content

    def render_to_rft_final_template(self, request, form):
        template = TemplateResponse(request, 'reports/rft_final_filter_form.html', {
            'final_filter_form': form,
        })
        template.render()
        return template.content

    def render_to_rft_overall_template(self, request, form):
        template = TemplateResponse(request, 'reports/rft_overall_filter_form.html', {
            'overall_filter_form': form,
        })
        template.render()
        return template.content

class RftSearchView(View):
    common = Common()
  
    def get_data_dict(self, info, date_list, rft_ok, not_ok, no_of_tractors, mark_data):
        data_dict = {
        'info': info + date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data,
        'no_of_tractors': no_of_tractors
        }
        return data_dict

    def overall(self,user, vin, date_list):
        rft_ok = []
        not_ok = []  
        no_of_tractors = []
        mark_data = []         
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))

            overall_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            
            rft_ok.append(overall_obj.filter(overall_status='RFT OK').count())
            not_ok.append(overall_obj.filter(overall_status='RFT NOT OK').count())
            # no_of_tractors.append(overall_obj.count())

            if overall_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((overall_obj.filter(overall_status='RFT OK').count()/float(len(overall_obj)))*100))
            else:
                percentage = 0
            no_of_tractors.append(percentage)    
            if len(overall_obj) != 0:
                percentage_dict={
                    'name': "Overall RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                mark_data.append(percentage_dict)
        data = self.get_data_dict('Overall RFT ', date_list, rft_ok, not_ok, no_of_tractors, mark_data)
        print data
        return data

    def final(self, user, vin, date_list):
        rft_ok = []
        not_ok = [] 
        no_of_tractors = []  
        mark_data = []    
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            final_obj = FinalRFT.objects.filter(vin__in=set(current_vin))

            rft_ok.append(final_obj.filter(final_status='RFT OK').count())
            not_ok.append(final_obj.filter(final_status='RFT NOT OK').count())
            # no_of_tractors.append(final_obj.count())

            if final_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((final_obj.filter(final_status='RFT OK').count()/float(len(final_obj)))*100))
            else:
                percentage = 0
            no_of_tractors.append(percentage)     
            if len(final_obj) != 0:
                percentage_dict={
                    'name': "Final RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                mark_data.append(percentage_dict)
        data = self.get_data_dict('Final RFT ', date_list, rft_ok, not_ok, no_of_tractors, mark_data)
        print data
        return data

    def rolldown(self, user, vin, date_list):
        rft_ok = []
        not_ok = []
        no_of_tractors = []
        mark_data = []
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            # current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            vin_status_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            rft_ok.append(vin_status_obj.filter(status='RFT OK').count())
            not_ok.append(vin_status_obj.filter(status='RFT NOT OK').count())
            # no_of_tractors.append(vin_status_obj.count())

            if vin_status_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_status_obj.filter(status='RFT OK').count()/float(len(vin_status_obj)))*100))
            else:
                percentage = 0
            no_of_tractors.append(percentage) 
            if len(vin_status_obj) != 0:
                percentage_dict={
                    'name': "Rolldown RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                mark_data.append(percentage_dict)
        data = self.get_data_dict('Rolldown RFT ', date_list, rft_ok, not_ok, no_of_tractors, mark_data)
        print data
        return data

    def post(self, request, *args, **kwargs):
        user=get_user_dict(request)
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        
        date_list = self.common.get_date_list(from_date, to_date)
        vin_obj = self.common.get_vin_details(user)
        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        rolldown = self.rolldown(user, vin, date_list)
        final = self.final(user, vin, date_list)
        overall = self.overall(user, vin, date_list)

        data = {
            'rolldown': rolldown,
            'final': final,
            'overall': overall
        }
        print data 
        return JsonResponse(data, safe=False)

class RftRolldownView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def rft_rolldown_chart_data(self, request, user, vin, form, date_list):
        for _date in date_list:
            # if user['plant'] == '':
            if form['form[rft_rolldown_plants]'] != [u'']:
                    vin = vin.filter(stations__cells__plants=int(form['form[rft_rolldown_plants]'][0]))
            # else:
            if 'form[rft_rolldown_markets]' in form and form['form[rft_rolldown_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[rft_rolldown_markets]'][0]))
            if 'form[rft_rolldown_shifts]' in form and form['form[rft_rolldown_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[rft_rolldown_shifts]'][0]))
            if 'form[rft_rolldown_base_models]' in form and form['form[rft_rolldown_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[rft_rolldown_base_models]'][0]))
            if 'form[rft_rolldown_models]' in form and form['form[rft_rolldown_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[rft_rolldown_models]'][0]))
            if 'form[rft_rolldown_stations]' in form and form['form[rft_rolldown_stations]'] != [u'']:
                vin = vin.filter(stations=int(form['form[rft_rolldown_stations]'][0]))
              
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            # current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            
            if 'rft_rolldown_stations' in request.POST and form['form[rft_rolldown_stations]'] != [u'']:
                vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            else:
                vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))
            # vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(status='RFT NOT OK').count())
            # self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0
            self.no_of_tractors.append(percentage)
            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Rolldown RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                self.mark_data.append(percentage_dict)
        data = {
        'info': 'Rolldown RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': self.rft_ok,
        'not_ok': self.not_ok,
        'no_of_tractors': self.no_of_tractors,
        'mark_data': self.mark_data
        }
        return data


    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        super(RftRolldownView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])
        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.rft_rolldown_chart_data(request, user, vin, form, date_list)

        return JsonResponse(data, safe=False)

class RftFinalView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def rft_final_chart_data(self, user, vin, form, date_list):
        for _date in date_list:
            # if user['plant'] == '':
            if form['form[rft_final_plants]'] != [u'']:
                vin = vin.filter(stations__cells__plants=int(form['form[rft_final_plants]'][0]))
            # else:
            if 'form[rft_final_markets]' in form and form['form[rft_final_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[rft_final_markets]'][0]))
            if 'form[rft_final_shifts]' in form and form['form[rft_final_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[rft_final_shifts]'][0]))
            if 'form[rft_final_base_models]' in form and form['form[rft_final_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[rft_final_base_models]'][0]))
            if 'form[rft_final_models]' in form and form['form[rft_final_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[rft_final_models]'][0]))
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin = vin.filter(stations=int(form['form[rft_final_stations]'][0]))
          
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            # current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            # else:
            #     vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            vin_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(final_status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(final_status='RFT NOT OK').count())
            # self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(final_status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0
            self.no_of_tractors.append(percentage)
            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Final RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                self.mark_data.append(percentage_dict)
        data = {
        'info': 'Final RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': self.rft_ok,
        'not_ok': self.not_ok,
        'no_of_tractors': self.no_of_tractors,
        'mark_data': self.mark_data
        }
        return data


    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        super(RftFinalView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.rft_final_chart_data(user, vin, form, date_list)

        return JsonResponse(data, safe=False)

class RftOverallView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def rft_overall_chart_data(self, user, vin, form, date_list):
        for _date in date_list:
            # if user['plant'] == '':
            if form['form[rft_overall_plants]'] != [u'']:
                vin = vin.filter(stations__cells__plants=int(form['form[rft_overall_plants]'][0]))
            # else:
            if 'form[rft_overall_markets]' in form and form['form[rft_overall_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[rft_overall_markets]'][0]))
            if 'form[rft_overall_shifts]' in form and form['form[rft_overall_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[rft_overall_shifts]'][0]))
            if 'form[rft_overall_base_models]' in form and form['form[rft_overall_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[rft_overall_base_models]'][0]))
            if 'form[rft_overall_models]' in form and form['form[rft_overall_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[rft_overall_models]'][0]))
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin = vin.filter(stations=int(form['form[rft_final_stations]'][0]))
              
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            # current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            # else:
            #     vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            vin_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(overall_status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(overall_status='RFT NOT OK').count())
            # self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(overall_status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0
            self.no_of_tractors.append(percentage)
            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Overall RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': percentage
                }
                self.mark_data.append(percentage_dict)
        data = {
        'info': 'Overall RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': self.rft_ok,
        'not_ok': self.not_ok,
        'no_of_tractors': self.no_of_tractors,
        'mark_data': self.mark_data
        }
        return data


    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        super(RftOverallView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.rft_overall_chart_data(user, vin, form, date_list)

        return JsonResponse(data, safe=False)

class DpuView(TemplateView):
    common = Common()
    template_name = 'reports/dpu.html'

    def get_context_data(self, **kwargs):
        user = get_user_dict(self.request)
        context = super(DpuView, self).get_context_data(**kwargs)
        rolldown_filter_form = DpuRolldownFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        final_filter_form = DpuFinalFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        overall_filter_form = DpuOverallFilterForm(
            user=get_user_dict(self.request),#get_user_dict(self.request),
            )
        context = {
            'username': user['user'],
            'rolldown_filter_form': rolldown_filter_form,
            'final_filter_form': final_filter_form,
            'overall_filter_form': overall_filter_form
        }
        return context

class DpuFilterView(View):

    def post(self, request):
        
        if 'dpu_rolldown_plants' in request.POST:
            rolldown_form = DpuRolldownFilterForm(user=get_user_dict(request), initial=request.POST)
            rolldown_filter_form = self.render_to_dpu_rolldown_template(request, rolldown_form)
            return JsonResponse(rolldown_filter_form, safe=False)
        if 'dpu_final_plants' in request.POST:
            final_form = DpuFinalFilterForm(user=get_user_dict(request), initial=request.POST)
            final_filter_form = self.render_to_dpu_final_template(request, final_form)
            return JsonResponse(final_filter_form, safe=False)
        if 'dpu_overall_plants' in request.POST:
            overall_form = DpuOverallFilterForm(user=get_user_dict(request), initial=request.POST)
            overall_filter_form = self.render_to_dpu_overall_template(request, overall_form)
            return JsonResponse(overall_filter_form, safe=False)

    def render_to_dpu_rolldown_template(self, request, form):
        template = TemplateResponse(request, 'reports/dpu_rolldown_filter.html', {
            'rolldown_filter_form': form,
        })
        template.render()
        return template.content

    def render_to_dpu_final_template(self, request, form):
        template = TemplateResponse(request, 'reports/dpu_final_filter.html', {
            'final_filter_form': form,
        })
        template.render()
        return template.content

    def render_to_dpu_overall_template(self, request, form):
        template = TemplateResponse(request, 'reports/dpu_overall_filter.html', {
            'overall_filter_form': form,
        })
        template.render()
        return template.content


class DpuSearchView(View):
    common = Common()

    def get_rolldown_dpu_by_date(self, date_list, vin):
        dpu_list = [] 
        mark_data = [] 
        defects_data = []
        sourcegates_list = ['DPU']
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            dpu_obj =  vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d')).exclude(stations__description='Final Inspection')
            check_point_defects = []
            part_defect = []
            if len(dpu_obj) != 0:
                    defect_rolldown = 0
                    for dpu in dpu_obj:
                        inspection_defects = InspectionDefects.objects.filter(vin=dpu).exclude(vin__stations__description='Final Inspection')
                        defect_rolldown  +=  inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints)
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect.append(sourcegate)
                                    except:
                                        part_defect_obj = ""

                    tractor_count = dpu_obj.count()
                    dpu = float("{0:.2f}".format(defect_rolldown/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            # import pdb;pdb.set_trace()
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        # import pdb;pdb.set_trace()
        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        print chart_defects   
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        return data

    def get_final_dpu_by_date(self, date_list, vin):
        dpu_list = [] 
        mark_data = []  
        defects_data = []
        sourcegates_list = ['DPU']
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            dpu_obj =  vin.filter(stations__description='Final Inspection').filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            check_point_defects = []
            part_defect = []
            if len(dpu_obj) != 0:
                    defect_final = 0
                    for dpu in dpu_obj:
                        inspection_defects =  InspectionDefects.objects.filter(vin=dpu).filter(vin__stations__description='Final Inspection')
                        defect_final += inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints)
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        #print "sourcegate", sourcegate
                                        check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect.append(sourcegate)
                                        #print "defect", sourcegate
                                    except:
                                        part_defect_obj = ""
                    tractor_count = dpu_obj.count()
                    dpu = float("{0:.2f}".format(defect_final/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    #print mark_dict
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            # import pdb;pdb.set_trace()
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        # import pdb;pdb.set_trace()
        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        print chart_defects 
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        return data

    def get_overall_dpu_by_date(self, date_list, vin):
        dpu_list = [] 
        mark_data = []   
        defects_data = []  
        sourcegates_list = ['DPU'] 
        for _date in date_list:
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            dpu_obj =  vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            check_point_defects = []
            part_defect = []
            if len(dpu_obj) != 0:
                    defect_overall = 0
                    for dpu in dpu_obj:
                        inspection_defects =  InspectionDefects.objects.filter(vin=dpu)
                        defect_overall  += inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints)
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        #print "sourcegate", sourcegate
                                        check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect.append(sourcegate)
                                        #print "defect", sourcegate
                                    except:
                                        part_defect_obj = ""
                    tractor_count = dpu_obj.count()
                    dpu = float("{0:.2f}".format(defect_overall/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            # import pdb;pdb.set_trace()
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        # import pdb;pdb.set_trace()
        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        print chart_defects 
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        return data


    def post(self, request, *args, **kwargs):
        user=get_user_dict(request)
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        vin_obj = self.common.get_vin_details(user) 

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])
        date_list = self.common.get_date_list(from_date, to_date)
        rolldown = self.get_rolldown_dpu_by_date(date_list, vin)
        final = self.get_final_dpu_by_date(date_list, vin)
        overall = self.get_overall_dpu_by_date(date_list, vin)
        data = {
            'rolldown': rolldown,
            'final': final,
            'overall': overall
        }
        #print data
        return JsonResponse(data, safe=False)

class DpuRolldownView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def dpu_rolldown_chart_data(self, request, user, vin, form, date_list):
        dpu_list = [] 
        mark_data = []  
        defects_data = []
        sourcegates_list = ['DPU']
        for _date in date_list:
            check_point_defects = []
            part_defect = []
            # import pdb;pdb.set_trace()
            # if user['plant'] == '':
            if form['form[dpu_rolldown_plants]'] != [u'']:
                    vin = vin.filter(stations__cells__plants=int(form['form[dpu_rolldown_plants]'][0]))
            # else:
            if 'form[dpu_rolldown_markets]' in form and form['form[dpu_rolldown_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[dpu_rolldown_markets]'][0]))
            if 'form[dpu_rolldown_shifts]' in form and form['form[dpu_rolldown_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[dpu_rolldown_shifts]'][0]))
            if 'form[dpu_rolldown_base_models]' in form and form['form[dpu_rolldown_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[dpu_rolldown_base_models]'][0]))
            if 'form[dpu_rolldown_models]' in form and form['form[dpu_rolldown_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[dpu_rolldown_models]'][0]))
            if 'form[dpu_rolldown_sourcegates]' in form and form['form[dpu_rolldown_sourcegates]'] != [u'']:
                sourcegates = SourceGates.objects.get(id=int(form['form[dpu_rolldown_sourcegates]'][0]))
                # print sourcegates
                defects = Defects.objects.filter(sourcegates = sourcegates)
                checkpoint_defects = CheckpointDefects.objects.filter(defects__in = defects)
                partdefects = PartDefects.objects.filter(defects__in = defects)           
                check_point_defect_list = []
                for check_point_defect in checkpoint_defects:
                    check_point_defect_list.append(check_point_defect.checkpoints.id)
                inspection_defect_vin = InspectionDefects.objects.filter(checkpoints__in=check_point_defect_list).values_list('vin',flat=True)    
                inspection_defect_vin_partdefect = InspectionDefects.objects.filter(partdefects__in = partdefects).values_list('vin',flat=True)
                vin_list = list(chain(inspection_defect_vin, inspection_defect_vin_partdefect))
                vin = vin.filter(id__in=vin_list)
                # print vin

              
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            current_vin = vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d')).exclude(stations__description='Final Inspection')
            if len(current_vin) != 0:
                    defect_overall = 0
                    for dpu in current_vin:
                        inspection_defects =  InspectionDefects.objects.filter(vin=dpu).exclude(vin__stations__description='Final Inspection')
                        defect_overall  += inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints).defects
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        check_point_defect_sourcegate_id = check_point_defect.defects.sourcegates.id
                                        if 'form[dpu_rolldown_sourcegates]' in form and form['form[dpu_rolldown_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_rolldown_sourcegates]'][0])
                                            if check_point_defect_sourcegate_id == sourcegate_id:
                                                check_point_defects.append(sourcegate)
                                        else:
                                            check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect_sourcegate_id = part_defect_obj.defects.sourcegates.id
                                        if 'form[dpu_rolldown_sourcegates]' in form and form['form[dpu_rolldown_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_rolldown_sourcegates]'][0])
                                            if part_defect_sourcegate_id == sourcegate_id:
                                                part_defect.append(sourcegate)
                                        else:
                                            part_defect.append(sourcegate)
                                    except:
                                        part_defect_obj = ""
                    tractor_count = current_vin.count()
                    dpu = float("{0:.2f}".format(defect_overall/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        #print chart_defects 
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        print data
        return data


    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        super(DpuRolldownView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])
        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.dpu_rolldown_chart_data(request, user, vin, form, date_list)
        #print data

        return JsonResponse(data, safe=False)

class DpuFinalView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def dpu_final_chart_data(self, request, user, vin, form, date_list):
        dpu_list = [] 
        mark_data = []  
        defects_data = []
        sourcegates_list = ['DPU']
        for _date in date_list:
            check_point_defects = []
            part_defect = []
            # if user['plant'] == '':
            if form['form[dpu_final_plants]'] != [u'']:
               vin = vin.filter(stations__cells__plants=int(form['form[dpu_final_plants]'][0]))
            # else:
            if 'form[dpu_fianl_markets]' in form and form['form[dpu_fianl_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[dpu_fianl_markets]'][0]))
            if 'form[dpu_final_shifts]' in form and form['form[dpu_final_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[dpu_final_shifts]'][0]))
            if 'form[dpu_fianl_base_models]' in form and form['form[dpu_final_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[dpu_final_base_models]'][0]))
            if 'form[dpu_final_models]' in form and form['form[dpu_final_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[dpu_final_models]'][0]))
            if 'form[dpu_final_sourcegates]' in form and form['form[dpu_final_sourcegates]'] != [u'']:
                # import pdb;pdb.set_trace()
                sourcegates = SourceGates.objects.get(id=int(form['form[dpu_final_sourcegates]'][0]))
                defects = Defects.objects.filter(sourcegates = sourcegates)
                check_point_defects = CheckpointDefects.objects.filter(defects__in = defects)
                partdefects = PartDefects.objects.filter(defects__in = defects)           
                check_point_defect_list = []
                for check_point_defect in check_point_defects:
                    check_point_defect_list.append(check_point_defect.checkpoints.id)
                #import pdb;pdb.set_trace()
                inspection_defect_vin = InspectionDefects.objects.filter(checkpoints__in=check_point_defect_list).values_list('vin',flat=True)    
                inspection_defect_vin_partdefect = InspectionDefects.objects.filter(partdefects__in = partdefects).values_list('vin',flat=True)
                vin_list = list(chain(inspection_defect_vin, inspection_defect_vin_partdefect))
                vin = vin.filter(id__in=vin_list)

              
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            dpu_obj =  vin.filter(stations__description='Final Inspection').filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            check_point_defects = []
            part_defect = []
            if len(dpu_obj) != 0:
                    defect_final = 0
                    for dpu in dpu_obj:
                        inspection_defects =  InspectionDefects.objects.filter(vin=dpu).filter(vin__stations__description='Final Inspection')
                        defect_final += inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints)
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        check_point_defect_sourcegate_id = check_point_defect.defects.sourcegates.id
                                        if 'form[dpu_final_sourcegates]' in form and form['form[dpu_final_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_final_sourcegates]'][0])
                                            if check_point_defect_sourcegate_id == sourcegate_id:
                                                check_point_defects.append(sourcegate)
                                        else:
                                            check_point_defects.append(sourcegate)
                                        # check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect_sourcegate_id = part_defect_obj.defects.sourcegates.id
                                        if 'form[dpu_final_sourcegates]' in form and form['form[dpu_final_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_final_sourcegates]'][0])
                                            if part_defect_sourcegate_id == sourcegate_id:
                                                part_defect.append(sourcegate)
                                        else:
                                            part_defect.append(sourcegate)
                                    except:
                                        part_defect_obj = ""
                    tractor_count = dpu_obj.count()
                    dpu = float("{0:.2f}".format(defect_final/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    #print mark_dict
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            # import pdb;pdb.set_trace()
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        # import pdb;pdb.set_trace()
        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        #print chart_defects 
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        return data



    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        #print request.POST
        super(DpuFinalView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])
        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.dpu_final_chart_data(request, user, vin, form, date_list)
        #print data

        return JsonResponse(data, safe=False)

class DpuOverallView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def dpu_overall_chart_data(self, request, user, vin, form, date_list):
        dpu_list = [] 
        mark_data = []  
        defects_data = []
        sourcegates_list = ['DPU']
        for _date in date_list:
            check_point_defects = []
            part_defect = []
            #import pdb;pdb.set_trace()
            if form['form[dpu_overall_plants]'] != [u'']:
               vin = vin.filter(stations__cells__plants=int(form['form[dpu_overall_plants]'][0]))
            # else:
            if 'form[dpu_overall_markets]' in form and form['form[dpu_overall_markets]'] != [u'']:
                vin = vin.filter(model__market=int(form['form[dpu_overall_markets]'][0]))
            if 'form[dpu_overall_shifts]' in form and form['form[dpu_overall_shifts]'] != [u'']:
                vin = vin.filter(shift=int(form['form[dpu_overall_shifts]'][0]))
            if 'form[dpu_overall_base_models]' in form and form['form[dpu_overall_base_models]'] != [u'']:
                vin = vin.filter(model__base_models=int(form['form[dpu_final_base_models]'][0]))
            if 'form[dpu_overall_models]' in form and form['form[dpu_overall_models]'] != [u'']:
                vin = vin.filter(model=int(form['form[dpu_overall_models]'][0]))
            if 'form[dpu_overall_sourcegates]' in form and form['form[dpu_overall_sourcegates]'] != [u'']:
                # import pdb;pdb.set_trace()
                sourcegates = SourceGates.objects.get(id=int(form['form[dpu_overall_sourcegates]'][0]))
                defects = Defects.objects.filter(sourcegates = sourcegates)
                checkpoint_defects = CheckpointDefects.objects.filter(defects__in = defects)
                partdefects = PartDefects.objects.filter(defects__in = defects)           
                check_point_defect_list = []
                for check_point_defect in checkpoint_defects:
                    check_point_defect_list.append(check_point_defect.checkpoints.id)
                #import pdb;pdb.set_trace()
                inspection_defect_vin = InspectionDefects.objects.filter(checkpoints__in=check_point_defect_list).values_list('vin',flat=True)    
                inspection_defect_vin_partdefect = InspectionDefects.objects.filter(partdefects__in = partdefects).values_list('vin',flat=True)
                vin_list = list(chain(inspection_defect_vin, inspection_defect_vin_partdefect))
                vin = vin.filter(id__in=vin_list)  
            my_date = datetime.strptime(_date, '%d-%m-%Y')
            dpu_obj =  vin.filter(timestamp__contains=datetime.strftime(my_date, '%Y-%m-%d'))
            # check_point_defects = []
            # part_defect = []
            if len(dpu_obj) != 0:
                    defect_overall = 0
                    for dpu in dpu_obj:
                        inspection_defects =  InspectionDefects.objects.filter(vin=dpu)
                        defect_overall  += inspection_defects.count()
                        if len(inspection_defects) !=0:
                            for inspection_defect in inspection_defects:
                                if inspection_defect.checkpoints != None:
                                    try:
                                        check_point_defect = CheckpointDefects.objects.get(
                                            checkpoints=inspection_defect.checkpoints)
                                        sourcegate =SourceGates.objects.get(id=check_point_defect.defects.sourcegates.id).description
                                        check_point_defect_sourcegate_id = check_point_defect.defects.sourcegates.id
                                        if 'form[dpu_overall_sourcegates]' in form and form['form[dpu_overall_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_overall_sourcegates]'][0])
                                            if check_point_defect_sourcegate_id == sourcegate_id:
                                                check_point_defects.append(sourcegate)
                                        else:
                                            check_point_defects.append(sourcegate)
                                        # check_point_defects.append(sourcegate)
                                    except:
                                        check_point_defect = ""
                                else:
                                    try:
                                        part_defect_obj = PartDefects.objects.get(id=inspection_defect.partdefects.id)
                                        sourcegate =SourceGates.objects.get(id=part_defect_obj.defects.sourcegates.id).description
                                        part_defect_sourcegate_id = part_defect_obj.defects.sourcegates.id
                                        if 'form[dpu_overall_sourcegates]' in form and form['form[dpu_overall_sourcegates]'] != [u'']:
                                            sourcegate_id = int(form['form[dpu_overall_sourcegates]'][0])
                                            if part_defect_sourcegate_id == sourcegate_id:
                                                part_defect.append(sourcegate)
                                        else:
                                            part_defect.append(sourcegate)
                                    except:
                                        part_defect_obj = ""
                    tractor_count = dpu_obj.count()
                    dpu = float("{0:.2f}".format(defect_overall/float(tractor_count)))
                    mark_dict={
                        'name': "Average",
                        'value': dpu,
                        'xAxis': _date,
                        'yAxis': dpu
                        }
                    mark_data.append(mark_dict)
            else:
                dpu = 0
            dpu_list.append(dpu)
            sourcegates = check_point_defects + part_defect
            d = {x:sourcegates.count(x) for x in sourcegates}
            # import pdb;pdb.set_trace()
            sourcegates_list.extend(sourcegates)
            defects_data.append(d)

        # import pdb;pdb.set_trace()
        source_list=list(set(sourcegates_list))

        chart_defects = []
        for source in source_list:
            defects_list =[]
            for defects in defects_data:
                if source in defects:
                    defects_list.append(defects[source])
                else:
                    defects_list.append(0)
            chart_defects.append(defects_list) 
        #print chart_defects 
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data,
        'source_list': source_list,
        'chart_defects': chart_defects
        }
        return data



    def removekey(self, dictionary, key):
        remove = dict(dictionary)
        del remove[key]
        return remove

    def post(self, request, *args, **kwargs):
        print request.POST
        super(DpuOverallView, self).__init__()
        user = get_user_dict(request)
        form = dict(request.POST)
        # form = {key: value for key, value in dict(request.POST).items() if value != [u'']}
        
        from_date = self.common.parse_date(form['from_date'][0])
        to_date = self.common.parse_date(form['to_date'][0]) 
        date_list = self.common.get_date_list(from_date, to_date)
        
        vin_obj = self.common.get_vin_details(user)

        date_from = parse(request.POST.get('from_date')).strftime('%Y-%d-%m %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%d-%m %H:%M:%S')

        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])
        print vin
        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.dpu_overall_chart_data(request, user, vin, form, date_list)
        #print data

        return JsonResponse(data, safe=False)


class SummaryView(FormView):
    common = Common()
    template_name = 'reports/summary.html'

    def get(self, request, *args, **kwargs):
        data = {
        'username': 'Guest User'
        }
        return render(request, self.template_name, data)



class SummarySearchView(View):
    common = Common()
    def post(self, request, *args, **kwargs):
        from_date =self.common.parse_date(
            request.POST.get('from_date'))
        to_date = self.common.parse_date(
            request.POST.get('to_date'))
        # plant = request.POST.get('plant')
        date_list = self.common.get_date_list(from_date, to_date)
        vin_status_and_rft = []        
        for _date in date_list:
            _date = _date.split('-')
            _date.reverse()
            rolldown_defects = 0
            final_defects = 0
            overall_defects = 0
            vin_status_obj = VinStatus.objects.filter(last_modified_date__contains='-'.join(_date))
            final_status_obj = FinalRFT.objects.filter(last_modified_date__contains='-'.join(_date))
            for vin_status in vin_status_obj:
                rolldown_defects += InspectionDefects.objects.filter(vin__vin=vin_status.vin).exclude(vin__stations__description='Final Inspection').count()
                final_defects += InspectionDefects.objects.filter(vin__vin=vin_status.vin).filter(vin__stations__description='Final Inspection').count()
                overall_defects += InspectionDefects.objects.filter(vin__vin=vin_status.vin).count()
            if len(vin_status_obj) != 0:
                if len(final_status_obj) != 0:
                    final_rft_ok = final_status_obj.filter(final_status='RFT OK').count()
                    final_rft_not_ok = final_status_obj.filter(final_status='RFT NOT OK').count()
                    overall_rft_ok = final_status_obj.filter(overall_status='RFT OK').count()
                    overall_rft_not_ok = final_status_obj.filter(overall_status='RFT NOT OK').count()
                else:
                    final_rft_ok = '-'
                    final_rft_not_ok = '-'
                    overall_rft_ok = '-'
                    overall_rft_not_ok = '-'

                vin_status_and_rft.append(
                    {
                        "date": vin_status_obj[len(vin_status_obj)-1].last_modified_date,
                        "no_of_tractors": len(vin_status_obj),
                        "rolldown_rft_ok": vin_status_obj.filter(status='RFT OK').count(),
                        "rolldown_rft_not_ok": vin_status_obj.filter(status='RFT NOT OK').count(),
                        "final_rft_ok": final_rft_ok,
                        "final_rft_not_ok": final_rft_not_ok,
                        "overall_rft_ok": overall_rft_ok,
                        "overall_rft_not_ok":overall_rft_not_ok,
                        "rolldown_dpu": float("{0:.2f}".format(rolldown_defects/float(len(vin_status_obj)))),
                        "final_dpu": float("{0:.2f}".format(final_defects/float(len(vin_status_obj)))),
                        "overall_dpu": float("{0:.2f}".format(overall_defects/float(len(vin_status_obj))))
                    }
                )
        print vin_status_and_rft
        response = self.render_to_template(vin_status_and_rft, request)
        return JsonResponse(response, safe=False)



    def render_to_template(self, vin_status_and_rft, request):
        template = TemplateResponse(request, 'reports/summary_table.html', {
            'items': vin_status_and_rft,
        })
        template.render()
        return template.content

class VinSummaryView(View):
    common = Common()
    def post(self, request, *args, **kwargs):
        vin_status=VinStatus.objects.filter(last_modified_date__contains=parse(request.POST.get('date')).strftime('%Y-%m-%d'))
        vin_status_and_final_rft = []
        for vin_status_obj in vin_status:
            model = Models.objects.get(id__in=VinDetails.objects.filter(vin=vin_status_obj.vin).values_list('model', flat=True))
            try:
                final_rft = FinalRFT.objects.get(vin=vin_status_obj.vin)
            except:
                final_rft = ""

            vin_status_and_final_rft.append({
                    "model": model,
                    "vin_status":vin_status_obj,
                    "final_rft":final_rft
            })
            

        response = self.render_to_template(vin_status_and_final_rft, request)
        return JsonResponse(response, safe=False)



    def render_to_template(self, vin_status_and_final_rft, request):
        template = TemplateResponse(request, 'reports/vin_table.html', {
            'datas': vin_status_and_final_rft,
        })
        template.render()
        return template.content        

class VinDetailsView(View):
    def post(self, request, *args, **kwargs):
        vin_number = request.POST.get("vin_number")
        verification = Verification.objects.filter(vin__vin=vin_number)

        response = self.render_to_template(verification, request, vin_number)
        inspection_defects = InspectionDefects.objects.filter(vin__vin = vin_number)
        inspection_defect_and_defect_closure = []
        for inspection_defect in inspection_defects:
            if inspection_defect.checkpoints:
                try:    
                    check_point_defect = CheckpointDefects.objects.get(
                        checkpoints=inspection_defect.checkpoints)
                except:
                    check_point_defect = ""
            else:
                check_point_defect = ""
            try:
                defects_closure = DefectClosure.objects.get(
                    inspection_defects = inspection_defect.id 
                )
            except:
                defects_closure = ""
            inspection_defect_and_defect_closure.append({
                "inspection_defect":inspection_defect,
                "defect_closure":defects_closure,
                "check_point_defect":check_point_defect

            })

        print inspection_defect_and_defect_closure
        inspection_defects_table = self.render_defect_details_to_template(
            inspection_defect_and_defect_closure, request
        )
        return JsonResponse({"vin_table":response,
            "inspection_defect_table":inspection_defects_table}, safe=False
        )

    def render_to_template(self, data, request, vin_number):
        template = TemplateResponse(request, 'reports/vin_details_table.html', {
            'datas': data,
            'vin_number':vin_number
        })
        template.render()
        return template.content

    def render_defect_details_to_template(self, data, request):
        template = TemplateResponse(request, 'reports/inspection_defect_details.html', {
            'datas': data,
        })
        template.render()
        return template.content        