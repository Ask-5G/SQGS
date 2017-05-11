
from django.shortcuts import render
from organization.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers, renderers
from rest_framework.authtoken.models import Token
from organization.authentication import SQGSTokenAuthentication
from .models import *
from reports.models import *                          
from organization.serializers import (PlantsSerializer, 
                                     CellsSerializer,  
                                     ShiftsSerializer, 
                                     StagesSerializer, 
                                     StationsSerializer,
                                     ModelStationsSerializer,
                                     RolesSerializer,
                                     UsersSerializer,
                                     AuthenticationSerializer,
                                     VerificationLogSerializer,
                                     SkillLevelSerializer,
                                     StageUserSerializer,
                                     DefectCategoriesSerializer,
                                     SourceGatesSerializer
                                     )
from organization.authentication import get_device_header, \
    validate_device_header
from django.http import HttpResponse



class ObtainAuthToken(APIView):
    def _assign_values(self, request):
        self.usercode = self.request.data.get("usercode", None)
        self.password = self.request.data.get("password", None)
        self.station = self.request.data.get("station", None)

    def post(self, request, *args, **kwargs):
        #import pdb;pdb.set_trace()
        self._assign_values(request)
        self.log_id = 0
        if self.usercode is not None and self.password is not None:
            try:
                self.user = Users.objects.get(user_code=self.usercode,\
                        password=self.password)
                if self.user.is_loggedin != True:
                    if self.station:
                        log = UserLog(
                            user = self.user,
                            station = Stations.objects.get(id=self.station)
                            )
                        log.save()
                        self.log_id = log.id
                    # if self.usercode != 'E0':
                    #     Users.objects.filter(user_code=self.usercode).update(is_loggedin=True)
                    self.data = {
                        'key': self.user.key,
                        'log': self.log_id
                    }
                
                    return Response({'data': self.data}, status=status.HTTP_201_CREATED)
                else: 
                    return Response({'data': "User already signed in" },status=status.HTTP_400_BAD_REQUEST)          
            except Users.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    def post(self, request, format=None):
        # Users.objects.filter(user_code=request.data.get('usercode')).update(is_loggedin=False)

        return Response({'data': "User logged out sucessfully!"}, status=status.HTTP_200_OK)


class VerificationLogView(APIView):

    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        try:
            log_obj = UserLog.objects.get(id=request.data.get('user_log'))
            stage_obj = Stages.objects.get(id=request.data.get('stage'))
            users = request.data.get('users')
            for user in users:
                user_obj = Users.objects.get(id=user)
                verification_log = VerificationLog(user_log=log_obj,
                    stages = stage_obj,
                    user = user_obj)
                verification_log.save()    
            return Response({'sucess':'Log saved sucessfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

                         
class PlantsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)


    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            plants = Plants.objects.filter(last_modified_date__gte=date)
        else:
            plants = Plants.objects.all()
        serializer = PlantsSerializer(plants, many=True)
        return Response({'plants': serializer.data})

class CellsView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            cells = Cells.objects.filter(last_modified_date__gte=date)
        else:
            cells = Cells.objects.all()
        serializer = CellsSerializer(cells, many=True)
        return Response({'cells': serializer.data})

class StagesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            stage = Stages.objects.filter(last_modified_date__gte=date)
        else:
            stage = Stages.objects.all()
        serializer = StagesSerializer(stage, many=True)
        return Response({'stages': serializer.data})

class  ModelStationsView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)
    
    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            model_station_stage =  ModelStations.objects.filter(last_modified_date__gte=date)
        else:
            model_station_stage =  ModelStations.objects.all()
        serializer =  ModelStationsSerializer(model_station_stage, many=True)
        return Response({'modelStations': serializer.data})

class StationsView(APIView):
  
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            station = Stations.objects.filter(last_modified_date__gte=date)
        else:
            station = Stations.objects.all()
        serializer = StationsSerializer(station, many=True)
        return Response({'stations': serializer.data})

class ShiftsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            shifts = Shifts.objects.filter(last_modified_date__gte=date)
        else:
            shifts = Shifts.objects.all()
        serializer = ShiftsSerializer(shifts, many=True)
        return Response({'shifts': serializer.data})

class RolesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        roles = Roles.objects.all()
        serializer = RolesSerializer(roles, many=True)
        return Response({'roles': serializer.data})

class UsersView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            users = Users.objects.filter(last_modified_date__gte=date)
        else:
            users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response({'users': serializer.data})

class SkilllevelView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            skilllevel = SkillLevel.objects.filter(last_modified_date__gte=date)
        else:
            skilllevel = SkillLevel.objects.all()
        serializer = SkillLevelSerializer(skilllevel, many=True)
        return Response({'skilllevel': serializer.data})

class StageUserView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            stageuser = StageUser.objects.filter(last_modified_date__gte=date)
        else:
            stageuser = StageUser.objects.all()
        serializer = StageUserSerializer(stageuser, many=True)
        return Response({'stageuser': serializer.data})

class DefectCategoriesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            defectcategories = DefectCategories.objects.filter(last_modified_date__gte=date)
        else:
            defectcategories = DefectCategories.objects.all()
        serializer = DefectCategoriesSerializer(defectcategories, many=True)
        return Response({'defectcategories': serializer.data})

class SourceGatesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            sourcegates = SourceGates.objects.filter(last_modified_date__gte=date)
        else:
            sourcegates = SourceGates.objects.all()
        serializer = SourceGatesSerializer(sourcegates, many=True)
        return Response({'sourcegates': serializer.data})







