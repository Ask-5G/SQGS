from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from basemodel.models import Models
from organization.models import * 
from inspection.models import VinStatus, VinDetails, Verification, DefectsPerUnit, FinalRFT, InspectionDefects
from datetime import date, datetime, timedelta as td
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from .forms import FilterForm
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from dateutil.parser import parse

class Common(object):

    def get_models(self, plant):
        if plant != None:
            plant_models = ModelStations.objects.filter(station__cells__plants=plant).values_list('model', flat=True)
            models = Models.objects.filter(id__in=set(plant_models))
        else:
            models = Models.objects.all()

        return models

    def get_stations(self, plant):
        if plant != None:
            return Stations.objects.filter(cells__plants=plant)
        else:
            return Stations.objects.all()

    def parse_date(self, date):
        return datetime.strptime(date, '%d-%m-%Y').date()

    def get_date_list(self, from_date, to_date):
        _date_list = []
        delta = to_date - from_date
        for i in range(delta.days + 1):
            _date = from_date + td(days=i)
            _date_list.append(_date.strftime('%d-%m-%Y'))
        return _date_list

    def get_rolldown_status_by_date(self, _date):
        _date = _date.split('-')
        _date.reverse()
        return VinStatus.objects.filter(last_modified_date__contains='-'.join(_date))

    def get_rolldown_status_by_model(self, _date, model):
        _date = _date.split('-')
        _date.reverse()
        vin = VinDetails.objects.filter(model=model).filter(timestamp__contains='-'.join(_date))
        vin_status_obj = VinStatus.objects.filter(vin__in=set(vin))
        return vin_status_obj

    def get_rolldown_status_by_station(self, _date, station):
        _date = _date.split('-')
        _date.reverse()
        vin_status_obj = Verification.objects.filter(stations=station).filter(timestamp__contains='-'.join(_date))
        return vin_status_obj

    def get_final_status_by_model(self, _date, model):
        _date = _date.split('-')
        _date.reverse()
        vin = VinDetails.objects.filter(model=model).filter(timestamp__contains='-'.join(_date))        
        final_obj = FinalRFT.objects.filter(vin__in=set(vin))
        #print final_obj
        #vin_status_obj = VinStatus.objects.filter(vin__in=set(vin))
        return final_obj


    def get_overall_status_by_model(self, _date, model):
        _date = _date.split('-')
        _date.reverse()
        vin = VinDetails.objects.filter(model=model).filter(timestamp__contains='-'.join(_date))        
        overall_obj = FinalRFT.objects.filter(vin__in=set(vin))
        #print overall_obj
        #vin_status_obj = VinStatus.objects.filter(vin__in=set(vin))
        return overall_obj

    def get_dpu_by_date(self, _date):
        _date = _date.split('-')
        _date.reverse()
        dpu_obj = DefectsPerUnit.objects.filter(date__contains='-'.join(_date))
        return dpu_obj

    def get_final_status_by_date(self, _date):
        _date = _date.split('-')
        _date.reverse()
        final_obj = FinalRFT.objects.filter(last_modified_date__contains='-'.join(_date))
        return final_obj

    def get_overall_status_by_date(self, _date):
        _date = _date.split('-')
        _date.reverse()
        overall_obj = FinalRFT.objects.filter(last_modified_date__contains='-'.join(_date))
        return overall_obj

class RftView(FormView):
    common = Common()
    template_name = 'reports/rft.html'

    def get(self, request, *args, **kwargs):
        plant = 1
        data = {
        'username': 'Guest User',
        'models': self.common.get_models(plant),
        'stations': self.common.get_stations(plant),
        }
        return render(request, self.template_name, data)	

class RftSearchView(View):
    common = Common()
  
    def overall(self, date_list):
        rft_ok = []
        not_ok = []  
        mark_data = []         
        for _date in date_list:
            overall_obj = self.common.get_overall_status_by_date(_date)

            rft_ok.append(overall_obj.filter(overall_status='RFT OK').count())
            not_ok.append(overall_obj.filter(overall_status='RFT NOT OK').count())
            if overall_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((overall_obj.filter(overall_status='RFT OK').count()/float(len(overall_obj)))*100))
            else:
                percentage = 0
                
            if len(overall_obj) != 0:
                percentage_dict={
                    'name': "Overall RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': overall_obj.filter(overall_status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Overall RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        return data

    def final(self, date_list):
        rft_ok = []
        not_ok = []   
        mark_data = []    
        for _date in date_list:
            final_obj = self.common.get_final_status_by_date(_date)

            rft_ok.append(final_obj.filter(final_status='RFT OK').count())
            not_ok.append(final_obj.filter(final_status='RFT NOT OK').count())
            if final_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((final_obj.filter(final_status='RFT OK').count()/float(len(final_obj)))*100))
            else:
                percentage = 0
                
            if len(final_obj) != 0:
                percentage_dict={
                    'name': "Final RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': final_obj.filter(final_status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Final RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        return data

    def rolldown(self, date_list):
        rft_ok = []
        not_ok = []
        mark_data = []
        for _date in date_list:
            vin_status_obj = self.common.get_rolldown_status_by_date(_date)

            rft_ok.append(vin_status_obj.filter(status='RFT OK').count())
            not_ok.append(vin_status_obj.filter(status='RFT NOT OK').count())
            if vin_status_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_status_obj.filter(status='RFT OK').count()/float(len(vin_status_obj)))*100))
            else:
                percentage = 0

            if len(vin_status_obj) != 0:
                percentage_dict={
                    'name': "Rolldown RFT(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_status_obj.filter(status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Rolldown RFT '+ date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }

        return data

    def post(self, request, *args, **kwargs):
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        rolldown = self.rolldown(date_list)
        final = self.final(date_list)
        overall = self.overall(date_list)
        data = {
            'rolldown': rolldown,
            'final': final,
            'overall': overall
        }
           
        return JsonResponse(data, safe=False)

class RftRolldownModelView(View):
    common = Common()

    def model_wise(self, date_list, model):
        rft_ok = []
        not_ok = []  
        mark_data = []     
        for _date in date_list:
            vin_status_obj = self.common.get_rolldown_status_by_model(_date, model)
            
            rft_ok.append(vin_status_obj.filter(status='RFT OK').count())
            not_ok.append(vin_status_obj.filter(status='RFT NOT OK').count())
            if vin_status_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_status_obj.filter(status='RFT OK').count()/float(len(vin_status_obj)))*100))
            else:
                percentage = 0

            if len(vin_status_obj) != 0:
                percentage_dict={
                    'name': "RFT Modelwise(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_status_obj.filter(status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Model- '+ Models.objects.get(id=model).description + ':' + date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        return data

    def post(self, request, *args, **kwargs):
        model = request.POST.get('model')
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        data = self.model_wise(date_list, model)

        return JsonResponse(data, safe=False)

class RftRolldownStationView(View):
    common = Common()

    def station_wise(self, date_list, station):
        rft_ok = []
        not_ok = []  
        mark_data = []   
        for _date in date_list:
            vin_status_obj = self.common.get_rolldown_status_by_station(_date, station)
            
            rft_ok.append(vin_status_obj.filter(status='RFT OK').count())
            not_ok.append(vin_status_obj.filter(status='RFT NOT OK').count())
            if vin_status_obj.filter(status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((vin_status_obj.filter(status='RFT OK').count()/float(len(vin_status_obj)))*100))
            else:
                percentage = 0

            if len(vin_status_obj) != 0:
                percentage_dict={
                    'name': "RFT Stationwise(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': vin_status_obj.filter(status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Station- '+ Stations.objects.get(id=station).description + ':' + date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        return data

    def post(self, request, *args, **kwargs):
        station = request.POST.get('station')
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        data = self.station_wise(date_list, station)

        return JsonResponse(data, safe=False)

class RftFinalModelView(View):
    common = Common()

    def model_wise(self, date_list, model):
        rft_ok = []
        not_ok = []  
        mark_data = []     
        for _date in date_list:
            final_status_obj = self.common.get_final_status_by_model(_date, model)  
            #print final_status_obj
            rft_ok.append(final_status_obj.filter(final_status='RFT OK').count())
            not_ok.append(final_status_obj.filter(final_status='RFT NOT OK').count())
            if final_status_obj.filter(final_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((final_status_obj.filter(final_status='RFT OK').count()/float(len(final_status_obj)))*100))
            else:
                percentage = 0

            if len(final_status_obj) != 0:
                percentage_dict={
                    'name': "RFT Modelwise(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': final_status_obj.filter(final_status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Model- '+ Models.objects.get(id=model).description + ':' + date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        #print data
        return data

    def post(self, request, *args, **kwargs):
        model = request.POST.get('model')
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        data = self.model_wise(date_list, model)

        return JsonResponse(data, safe=False)

class RftOverallModelView(View):
    common = Common()

    def model_wise(self, date_list, model):
        rft_ok = []
        not_ok = []  
        mark_data = []     
        for _date in date_list:
            overall_status_obj = self.common.get_overall_status_by_model(_date, model)   
            rft_ok.append(overall_status_obj.filter(overall_status='RFT OK').count())
            not_ok.append(overall_status_obj.filter(overall_status='RFT NOT OK').count())
            if overall_status_obj.filter(overall_status='RFT OK').count() != 0:
                percentage = float("{0:.2f}".format((overall_status_obj.filter(overall_status='RFT OK').count()/float(len(overall_status_obj)))*100))
            else:
                percentage = 0

            if len(overall_status_obj) != 0:
                percentage_dict={
                    'name': "RFT Modelwise(%)",
                    'value': percentage,
                    'xAxis': _date,
                    'yAxis': overall_status_obj.filter(overall_status='RFT OK').count()
                }
                mark_data.append(percentage_dict)
        data = {
        'info': 'Model- '+ Models.objects.get(id=model).description + ':' + date_list[0] + ' to ' + date_list[len(date_list)-1],
        'date_list': date_list,
        'rft_ok': rft_ok,
        'not_ok': not_ok,
        'mark_data': mark_data
        }
        return data

    def post(self, request, *args, **kwargs):
        model = request.POST.get('model')
        from_date = self.common.parse_date(request.POST.get('from_date'))
        to_date = self.common.parse_date(request.POST.get('to_date')) 
        date_list = self.common.get_date_list(from_date, to_date)
        data = self.model_wise(date_list, model)

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
            print date_list
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