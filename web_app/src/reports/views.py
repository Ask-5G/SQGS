from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from basemodel.models import Models
from organization.models import * 
from inspection.models import VinStatus, VinDetails, Verification, DefectsPerUnit, FinalRFT, InspectionDefects
from datetime import date, datetime, timedelta as td
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .forms import RftRolldownFilterForm, RftFinalFilterForm, RftOverallFilterForm
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from dateutil.parser import parse

def get_user_dict(request):
    return {
        "user": 'Guest User',
        "plant": 1
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

    def get_dpu_by_date(self, _date):
        _date = _date.split('-')
        _date.reverse()
        dpu_obj = DefectsPerUnit.objects.filter(date__contains='-'.join(_date))
        return dpu_obj

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
        if 'rft_rolldown_markets' in request.POST:
            rolldown_form = RftRolldownFilterForm(user=get_user_dict(request), initial=request.POST)
            rolldown_filter_form = self.render_to_rft_rolldown_template(request, rolldown_form)
            return JsonResponse(rolldown_filter_form, safe=False)
        if 'rft_final_markets' in request.POST:
            final_form = RftFinalFilterForm(user=get_user_dict(request), initial=request.POST)
            final_filter_form = self.render_to_rft_final_template(request, final_form)
            return JsonResponse(final_filter_form, safe=False)
        if 'rft_overall_markets' in request.POST:
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
  
    def overall(self,user, vin, date_list):
        rft_ok = []
        not_ok = []  
        no_of_tractors = []
        mark_data = []         
        for _date in date_list:
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            overall_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            
            rft_ok.append(overall_obj.filter(overall_status='RFT OK').count())
            not_ok.append(overall_obj.filter(overall_status='RFT NOT OK').count())
            no_of_tractors.append(overall_obj.count())

            if overall_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((overall_obj.filter(overall_status='RFT OK').count()/float(len(overall_obj)))*100))
            else:
                percentage = 0
                
            if len(overall_obj) != 0:
                percentage_dict={
                    'name': "Overall RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': overall_obj.count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Overall RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data,
        'no_of_tractors': no_of_tractors
        }
        return data

    def final(self, user, vin, date_list):
        rft_ok = []
        not_ok = [] 
        no_of_tractors = []  
        mark_data = []    
        for _date in date_list:
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            final_obj = FinalRFT.objects.filter(vin__in=set(current_vin))

            rft_ok.append(final_obj.filter(final_status='RFT OK').count())
            not_ok.append(final_obj.filter(final_status='RFT NOT OK').count())
            no_of_tractors.append(final_obj.count())

            if final_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((final_obj.filter(final_status='RFT OK').count()/float(len(final_obj)))*100))
            else:
                percentage = 0
                
            if len(final_obj) != 0:
                percentage_dict={
                    'name': "Final RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': final_obj.count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Final RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'no_of_tractors': no_of_tractors,
        'mark_data': mark_data
        }
        return data

    def rolldown(self, user, vin, date_list):
        rft_ok = []
        not_ok = []
        no_of_tractors = []
        mark_data = []
        for _date in date_list:
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            vin_status_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            rft_ok.append(vin_status_obj.filter(status='RFT OK').count())
            not_ok.append(vin_status_obj.filter(status='RFT NOT OK').count())
            no_of_tractors.append(vin_status_obj.count())

            if vin_status_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_status_obj.filter(status='RFT OK').count()/float(len(vin_status_obj)))*100))
            else:
                percentage = 0

            if len(vin_status_obj) != 0:
                percentage_dict={
                    'name': "Rolldown RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_status_obj.count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Rolldown RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'no_of_tractors':no_of_tractors,
        'mark_data': mark_data
        }

        return data

    def post(self, request, *args, **kwargs):
        user=get_user_dict(request)
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        print date_list
        vin_obj = self.common.get_vin_details(user)
        date_from = parse(request.POST.get('from_date')).strftime('%Y-%m-%d %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%m-%d %H:%M:%S')
        print date_from + date_to
        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        rolldown = self.rolldown(user, vin, date_list)
        final = self.final(user, vin, date_list)
        overall = self.overall(user, vin, date_list)

        data = {
            'rolldown': rolldown,
            'final': final,
            'overall': overall
        }
           
        return JsonResponse(data, safe=False)

class RftRolldownView(View):
    common = Common()
    
    def __init__(self):
        self.rft_ok = []
        self.not_ok = []  
        self.mark_data = []  
        self.no_of_tractors = []

    def rft_rolldown_chart_data(self, user, vin, form, date_list):
        for _date in date_list:
            if user['plant'] == '':
                if form['form[rft_rolldown_plants]'] != [u'']:
                    vin = vin.filter(stations__cells__plants=int(form['form[rft_rolldown_plants]'][0]))
            else:
                if form['form[rft_rolldown_markets]'] != [u'']:
                    vin = vin.filter(model__market=int(form['form[rft_rolldown_markets]'][0]))
                # if form['form[rft_rolldown_shifts]'] != [u'']:
                #     vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m')).filter(model__markets=form['form[rft_rolldown_markets]'][0])
                if form['form[rft_rolldown_base_models]'] != [u'']:
                    vin = vin.filter(model__base_models=int(form['form[rft_rolldown_base_models]'][0]))
                if form['form[rft_rolldown_models]'] != [u'']:
                    vin = vin.filter(model=int(form['form[rft_rolldown_models]'][0]))
                if form['form[rft_rolldown_stations]'] != [u'']:
                    vin = vin.filter(stations=int(form['form[rft_rolldown_stations]'][0]))
              
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            
            if form['form[rft_rolldown_stations]'] != [u'']:
                vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            else:
                vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(status='RFT NOT OK').count())
            self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0

            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Rolldown RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_obj.count()
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
        date_from = parse(request.POST.get('from_date')).strftime('%Y-%m-%d %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%m-%d %H:%M:%S')
        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.rft_rolldown_chart_data(user, vin, form, date_list)

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
            if user['plant'] == '':
                if form['form[rft_final_plants]'] != [u'']:
                    vin = vin.filter(stations__cells__plants=int(form['form[rft_final_plants]'][0]))
            else:
                if form['form[rft_final_markets]'] != [u'']:
                    vin = vin.filter(model__market=int(form['form[rft_final_markets]'][0]))
                # if form['form[rft_final_shifts]'] != [u'']:
                #     vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m')).filter(model__markets=form['form[rft_final_markets]'][0])
                if form['form[rft_final_base_models]'] != [u'']:
                    vin = vin.filter(model__base_models=int(form['form[rft_final_base_models]'][0]))
                if form['form[rft_final_models]'] != [u'']:
                    vin = vin.filter(model=int(form['form[rft_final_models]'][0]))
                # if form['form[rft_final_stations]'] != [u'']:
                #     vin = vin.filter(stations=int(form['form[rft_final_stations]'][0]))
              
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            # else:
            #     vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            vin_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(final_status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(final_status='RFT NOT OK').count())
            self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(final_status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0

            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Final RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_obj.count()
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
        date_from = parse(request.POST.get('from_date')).strftime('%Y-%m-%d %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%m-%d %H:%M:%S')
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
            if user['plant'] == '':
                if form['form[rft_overall_plants]'] != [u'']:
                    vin = vin.filter(stations__cells__plants=int(form['form[rft_overall_plants]'][0]))
            else:
                if form['form[rft_overall_markets]'] != [u'']:
                    vin = vin.filter(model__market=int(form['form[rft_overall_markets]'][0]))
                # if form['form[rft_final_shifts]'] != [u'']:
                #     vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m')).filter(model__markets=form['form[rft_final_markets]'][0])
                if form['form[rft_overall_base_models]'] != [u'']:
                    vin = vin.filter(model__base_models=int(form['form[rft_overall_base_models]'][0]))
                if form['form[rft_overall_models]'] != [u'']:
                    vin = vin.filter(model=int(form['form[rft_overall_models]'][0]))
                # if form['form[rft_final_stations]'] != [u'']:
                #     vin = vin.filter(stations=int(form['form[rft_final_stations]'][0]))
              
            current_vin = vin.filter(timestamp__contains=parse(_date).strftime('%Y-%d-%m'))
            
            # if form['form[rft_final_stations]'] != [u'']:
            #     vin_obj = Verification.objects.filter(vin__in=set(current_vin))
            # else:
            #     vin_obj = VinStatus.objects.filter(vin__in=set(current_vin))

            vin_obj = FinalRFT.objects.filter(vin__in=set(current_vin))
            self.rft_ok.append(vin_obj.filter(overall_status='RFT OK').count())
            self.not_ok.append(vin_obj.filter(overall_status='RFT NOT OK').count())
            self.no_of_tractors.append(vin_obj.count())

            if vin_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_obj.filter(overall_status='RFT OK').count()/float(len(vin_obj)))*100))
            else:
                percentage = 0

            if len(vin_obj) != 0:
                percentage_dict={
                    'name': "Overall RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_obj.count()
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
        date_from = parse(request.POST.get('from_date')).strftime('%Y-%m-%d %H:%M:%S')
        date_to = parse(request.POST.get('to_date')).strftime('%Y-%m-%d %H:%M:%S')
        vin = vin_obj.extra(where=["timestamp >= '%s' and timestamp <= '%s'"%(date_from,date_to)])

        # form = [self.removekey(form, key) for key in ['from_date', 'to_date']]
        data = self.rft_overall_chart_data(user, vin, form, date_list)

        return JsonResponse(data, safe=False)

class DpuView(FormView):
    common = Common()
    template_name = 'reports/dpu.html'

    def get(self, request, *args, **kwargs):
        data = {
        'username': 'Guest User'
        }
        return render(request, self.template_name, data)

class DpuSearchView(View):
    common = Common()
 
    def day_wise(self, date_list):
        dpu_list = [] 
        mark_data = []      
        for _date in date_list:
            dpu_obj = self.common.get_dpu_by_date(_date)
            if len(dpu_obj) != 0:
                dpu = dpu_obj[0].dpu
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
        print mark_data
        data = {
        'date_list': date_list,
        'dpu': dpu_list,
        'mark_data': mark_data
        }
        return data

    def post(self, request, *args, **kwargs):

        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        data = self.day_wise(date_list)
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
            try:
                final_rft = FinalRFT.objects.get(vin=vin_status_obj.vin)
            except:
                final_rft = ""

            vin_status_and_final_rft.append({
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
        print inspection_defects
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