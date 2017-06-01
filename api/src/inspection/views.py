from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base64 import b64decode
from django.core.files.base import ContentFile
from django.utils import timezone
from organization.authentication import SQGSTokenAuthentication
from inspection.models import InspectionDefects, DefectClosure, VinDetails, Verification, VinStatus, DefectsPerUnit, FinalRFT
from inspection.serializers import InspectionDefectsSerializer, DefectClosureSerializer, VinDetailsSerializer, ReportSerializer, FinalRFTSerializer
from checkpoints.models import *
from reports.models import *
from datetime import datetime, timedelta, time
from reports.views import get_queryset

class VinDetailsView(APIView):        

    authentication_classes = (SQGSTokenAuthentication,)

    def cmd_verification(self, vindetails, stations):
        verification = Verification(
            vin = vindetails,
            stations = stations,
            defects_count = 0,
            closure_count = 0,
            status = 'RFT NOT OK'
            )
        verification.save()

    def vin_create(self, vin_num, models, users, stations, shifts, plants, vin_order):
        vindetails = VinDetails(
            vin = vin_num, 
            model = models, 
            users = users,
            stations = stations,
            shift = shifts,
            plant = plants,
            vin_order = vin_order
         )
        vindetails.save()
        self.cmd_verification(vindetails, stations)
        return vindetails

    def get(self, request, format=None):
        vindetails = get_queryset(request, VinDetails)
        serializer = VinDetailsSerializer(vindetails, many=True)
        return Response({'vin_details': serializer.data})

    def post(self, request, format=None):
        vin_num = request.data.get('vin')
        models = Models.objects.get(id=request.data.get('model'))
        users = Users.objects.get(id=request.data.get('users'))
        stations = Stations.objects.get(id=request.data.get('stations'))
        shifts = Shifts.objects.get(id=request.data.get('shift'))
        plants = Plants.objects.get(id=request.data.get('plant'))
        vin_order = request.data.get('vin_order')
        vin_obj = VinDetails.objects.filter(vin=vin_num)
        if stations.description != 'Final Inspection':
            if len(vin_obj) != 0:
                for vin in vin_obj:
                    inspection_defects = InspectionDefects.objects.filter(vin=vin.id)
                    defects = inspection_defects.values_list('id', flat=True)
                    defect_closure = DefectClosure.objects.filter(inspection_defects__in=defects)
                    if inspection_defects.count() == defect_closure.count():
                        Verification.objects.filter(vin=vin.id, stations=vin.stations).update(defects_count = inspection_defects.count(),\
                            closure_count = defect_closure.count(),status='RFT OK')
                    else:
                        Verification.objects.filter(vin=vin.id, stations=vin.stations).update(defects_count = inspection_defects.count(),\
                            closure_count = defect_closure.count(),status='RFT NOT OK')
                vindetails = self.vin_create(vin_num, models, users, stations, shifts, plants, vin_order)
                vin_list = vin_obj.values_list('id', flat=True)
                tot_defects = InspectionDefects.objects.filter(vin__in=vin_list).count()
                tot_closure = DefectClosure.objects.filter(inspection_defects__vin__in=vin_list).count()
                if tot_defects == tot_closure:
                    rep_status = 'RFT OK'
                else:
                    rep_status = 'RFT NOT OK'
                
                vin_status = VinStatus.objects.filter(vin=vin_num).update(
                    tot_defects = tot_defects,
                    tot_closure = tot_closure,
                    status = rep_status
                    )
            else:
                vindetails = self.vin_create(vin_num, models, users, stations, shifts, plants, vin_order)
                vin_status = VinStatus(
                    vin = vin_num,
                    tot_defects = 0,
                    tot_closure = 0,
                    status = 'RFT NOT OK'
                    )
                vin_status.save()
        else:
            vindetails = VinDetails(
            vin = vin_num, 
            model = models, 
            users = users,
            stations = stations,
            shift = shifts,
            plant = plants,
            vin_order = vin_order
            )
            vindetails.save()
        serializer = VinDetailsSerializer(vindetails)
        return Response({'vin_details': serializer.data}, status=status.HTTP_201_CREATED)

class InspectionDefectsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)
    def _assign_values(self, request):
        self.image_1 = self.request.data.get('image_1')
        self.partdefects = self.request.data.get('partdefects')
        self.vin = self.request.data.get('vin')
        self.observations = request.data.get('observations')
        self.image_2 = request.data.get('image_2')
        self.image_quadrant = request.data.get('image_quadrant')
        self.checkpoints = request.data.get('checkpoints')
        self.created_time = request.data.get('created_time')
        self.updated_time = request.data.get('updated_time')
        self.user = request.data.get('user')

    def _save_image(self):
        self.image_1 = b64decode(self.image_1.replace(
        "data:image/jpeg;base64,", ""))
        self.completed_image = ContentFile(
        self.image_1, '{0}-{1}.jpg'.format(self.partdefects, self.vin))
        self.image = Images(related_to='InspectionDefects',
            description='{0}-{1}'.format(self.partdefects,self.vin),
            image=self.completed_image
            )
        self.image.save()

    def _get_vin_obj(self):
        self.vin_obj = VinDetails.objects.get(id=self.vin)

    def _get_user_obj(self):
        self.user_obj = Users.objects.get(id=self.user)

    def _get_image_1_obj(self):
        try:
            self.image_1_obj = Images.objects.get(id=self.image.id)
        except Exception as e:
            self.image_1_obj = ''

    def _get_checkpoints_obj(self):
        try:
            self.checkpoints_obj = Checkpoints.objects.get(id=self.checkpoints)
        except Exception as e:
            self.checkpoints_obj = ''

    def _get_partdefects_obj(self):
        try:
            self.partdefects_obj = PartDefects.objects.get(id=self.partdefects)
        except Exception as e:
            self.partdefects_obj = ''

    def get(self, request, format=None):
        inspectiondefects = get_queryset(request, InspectionDefects)
        serializer = InspectionDefectsSerializer(inspectiondefects, many=True)
        return Response({'inspection_defects': serializer.data})

    def post(self, request, format=None):
        self._assign_values(request)
        if "image_1" in request.data and self.image_1 != '':
            self._save_image()
		
        self._get_vin_obj()
        self._get_image_1_obj()
        self._get_checkpoints_obj()
        self._get_partdefects_obj()
        self._get_user_obj()
        
        if self.image_1_obj != '' and self.partdefects_obj !=  '':
			self.inspection_defects = InspectionDefects(vin=self.vin_obj, observations=self.observations, image_1=self.image_1_obj, image_quadrant = self.image_quadrant,
			partdefects = self.partdefects_obj, user = self.user_obj, created_time = self.created_time, updated_time = self.updated_time)
        elif self.image_1_obj == '' and self.partdefects_obj !=  '':	
			self.inspection_defects = InspectionDefects(vin=self.vin_obj, observations=self.observations, image_quadrant = self.image_quadrant,
			partdefects = self.partdefects_obj, user = self.user_obj, created_time = self.created_time, updated_time = self.updated_time)
        else:
			self.inspection_defects = InspectionDefects(vin=self.vin_obj, observations=self.observations, image_quadrant = self.image_quadrant,
			checkpoints = self.checkpoints_obj, user = self.user_obj, created_time = self.created_time, updated_time = self.updated_time)
        self.inspection_defects.save()
        defects_count = InspectionDefects.objects.filter(vin=self.vin).count()
        verication = Verification.objects.filter(vin=self.vin)
        verication.update(defects_count=defects_count)
        serializer = InspectionDefectsSerializer(self.inspection_defects)
        return Response({'inspection_defects':serializer.data}, status=status.HTTP_201_CREATED)
		
class DefectClosureView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        defectclosure = get_queryset(request, DefectClosure)
        serializer = DefectClosureSerializer(defectclosure, many=True)
        return Response({'defect_closure': serializer.data})


    def post(self, request, format=None):
        serializer = DefectClosureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'defect_closure': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class ReportView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        try:
            vin_obj = VinDetails.objects.filter(vin=request.data.get('vin'))
            vin_list = vin_obj.exclude(stations=request.data.get('station')).values_list('id',flat=True)
            tot_defects = InspectionDefects.objects.filter(vin__in=vin_list).count()
            tot_closure = DefectClosure.objects.filter(inspection_defects__vin__in=vin_list).count()
            if len(vin_obj) != 0:
                for vin in vin_obj:
                    inspection_defects = InspectionDefects.objects.filter(vin=vin.id)
                    defects = inspection_defects.values_list('id', flat=True)
                    defect_closure = DefectClosure.objects.filter(inspection_defects__in=defects)
                    if inspection_defects.count() == defect_closure.count():
                        Verification.objects.filter(vin=vin.id, stations=vin.stations).update(defects_count = inspection_defects.count(),\
                            closure_count = defect_closure.count(),status='RFT OK')
                    else:
                        Verification.objects.filter(vin=vin.id, stations=vin.stations).update(defects_count = inspection_defects.count(),\
                            closure_count = defect_closure.count(),status='RFT NOT OK')
            if tot_defects == tot_closure:
                rep_status = 'RFT OK'
            else:
                rep_status = 'RFT NOT OK'
            
            if rep_status == 'RFT OK':
                vin_list = vin_obj.values_list('id', flat=True)
                tot_defects = InspectionDefects.objects.filter(vin__in=vin_list).count()
                tot_closure = DefectClosure.objects.filter(inspection_defects__vin__in=vin_list).count()


                if tot_defects == tot_closure:
                    if len(vin_obj) != request.data.get('station'):
                        rep_status = 'RFT NOT OK'
                elif tot_defects != tot_closure:                                        
                    rep_status = 'RFT NOT OK'

                vin_status = VinStatus.objects.filter(vin=request.data.get('vin')).update(
                    tot_defects = tot_defects, 
                    tot_closure = tot_closure,
                    status = rep_status
                    )

            tractors = VinStatus.objects.filter(last_modified_date__gte=datetime.combine(datetime.now().date(), time()))
            station_wise_defects = 0
            track_count = 0
            
            for tracktore in tractors:
                station_wise_defects += InspectionDefects.objects.filter(vin__vin=tracktore.vin).exclude(vin__stations__description='Final Inspection').count()
                track_count += 1
            
            dpu_obj = DefectsPerUnit.objects.filter(date__gte=datetime.combine(datetime.now().date(), time()))
            
            if len(dpu_obj) != 0:
                dpu_obj.update(no_of_defects = station_wise_defects, no_of_tractors = track_count, dpu = float("{0:.2f}".format(station_wise_defects/float(track_count))))
            else:    
                defects_per_unit = DefectsPerUnit(
                    no_of_defects = station_wise_defects,
                    no_of_tractors = track_count,
                    dpu = float("{0:.2f}".format(station_wise_defects/float(track_count))),
                    )
                defects_per_unit.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VinstatusView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
            vin = request.data.get('vin')
            station = request.data.get('station') 
            vin_obj = VinDetails.objects.get(vin=vin, stations=station)   
            inspection_defects = InspectionDefects.objects.filter(vin=vin_obj)
            defect_closure = DefectClosure.objects.filter(inspection_defects__vin=vin_obj)
            if inspection_defects.count() == defect_closure.count(): 
                status = 'RFT OK'
                verification = Verification(
                    vin = vin,
                    stations = station,
                    defects_count = inspection_defects.count(),
                    closure_count = defect_closure.count(),
                    status = status
                    )
                verification.save()
                return Response({'success':'True'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinalReportView(APIView):
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        vin_num = request.data.get('vin')
        station = request.data.get('station') 
        final_status = request.data.get('rft_status')
        vin_obj = VinDetails.objects.get(vin=vin_num, stations=station) 
        stations = Stations.objects.get(id=station)  
        inspection_defects = InspectionDefects.objects.filter(vin=vin_obj)
        defect_closure = DefectClosure.objects.filter(inspection_defects__vin=vin_obj)
        if inspection_defects.count() == defect_closure.count(): 
            verify_status = 'RFT OK'
        else:
            verify_status = 'RFT NOT OK'
        verification = Verification(
            vin = vin_obj,
            stations = stations,
            defects_count = inspection_defects.count(),
            closure_count = defect_closure.count(),
            status = verify_status
            )
        verification.save()
        overall_status = self.find_overall_status(vin_num, final_status)
        final_rft = FinalRFT(
            vin = vin_num, 
            final_status = final_status, 
            overall_status = overall_status,
            )
        final_rft.save()
        serializer = FinalRFTSerializer(final_rft)
        return Response({'final_rft': serializer.data}, status=status.HTTP_201_CREATED)

    
    def find_overall_status(self, vin_num, final_status):
        vin = VinStatus.objects.get(vin = vin_num)
        if vin.status == "RFT OK" and final_status == "RFT OK":
            return "RFT OK"
        else:
            return "RFT NOT OK"
