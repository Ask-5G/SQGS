from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organization.authentication import SQGSTokenAuthentication
from checkpoints.models import ( 
                                Defects, 
                                InspectionTypes,
                                PartDefects,
                                Repairs,
                                Checkpoints, 
                                CheckpointDefects,
                                Checklist
                                )

from checkpoints.serializers import ( 
                                     DefectsSerializer,
                                     InspectionTypesSerializer,
                                     PartDefectsSerializer, 
                                     RepairsSerializer,
                                     CheckpointsSerializer,
                                     CheckpointDefectsSerializer,
                                     ChecklistSerializer
                                     )


class DefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            defects = Defects.objects.filter(last_modified_date__gte=date)
        else:
            defects = Defects.objects.all()
        serializer = DefectsSerializer(defects, many=True)
        return Response({'defects': serializer.data})

class InspectionTypesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        inspectiontypes = InspectionTypes.objects.all()
        serializer = InspectionTypesSerializer(inspectiontypes, many=True)
        return Response({'inspectiontypes': serializer.data})

    
class PartDefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            partdefects = PartDefects.objects.filter(last_modified_date__gte=date)
        else:
            partdefects = PartDefects.objects.all()
        serializer = PartDefectsSerializer(partdefects, many=True)
        print serializer.data
        return Response({'partdefects': serializer.data})

    def post(self, request, format=None):
        serializer = PartDefectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RepairsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            repairs = Repairs.objects.objects.filter(last_modified_date__gte=date)
        else:
            repairs = Repairs.objects.all()
        serializer = RepairsSerializer(repairs, many=True)
        return Response({'repairs': serializer.data})

class CheckpointsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            checkpoints = Checkpoints.objects.filter(last_modified_date__gte=date)
        else:
            checkpoints = Checkpoints.objects.all()
        serializer = CheckpointsSerializer(checkpoints, many=True)
        return Response({'checkpoints': serializer.data})

class CheckpointDefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)
    
    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            checkpoints_defect = CheckpointDefects.objects.filter(last_modified_date__gte=date)
        else:
            checkpoints_defect = CheckpointDefects.objects.all()
        serializer = CheckpointDefectsSerializer(checkpoints_defect, many=True)
        return Response({'checkpoints_defect': serializer.data})

class ChecklistView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)
    
    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            checklist = Checklist.objects.filter(last_modified_date__gte=date)
        else:
            checklist = Checklist.objects.all()
        serializer = ChecklistSerializer(checklist, many=True)
        return Response({'checklist': serializer.data})

    def post(self, request, format=None):
        serializer = ChecklistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
