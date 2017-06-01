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
from reports.views import get_queryset


class DefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        defects = get_queryset(request, Defects)
        serializer = DefectsSerializer(defects, many=True)
        return Response({'defects': serializer.data})

class InspectionTypesView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        inspectiontypes = get_queryset(request, InspectionTypes)
        serializer = InspectionTypesSerializer(inspectiontypes, many=True)
        return Response({'inspectiontypes': serializer.data})

    
class PartDefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        partdefects = get_queryset(request, PartDefects)
        serializer = PartDefectsSerializer(partdefects, many=True)
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
        repairs = get_queryset(request, Repairs)
        serializer = RepairsSerializer(repairs, many=True)
        return Response({'repairs': serializer.data})

class CheckpointsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        checkpoints = get_queryset(request, Checkpoints)
        serializer = CheckpointsSerializer(checkpoints, many=True)
        return Response({'checkpoints': serializer.data})

class CheckpointDefectsView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)
    
    def get(self, request, format=None):
        checkpoints_defect = get_queryset(request, CheckpointDefects)
        serializer = CheckpointDefectsSerializer(checkpoints_defect, many=True)
        return Response({'checkpoints_defect': serializer.data})

class ChecklistView (APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)
    
    def get(self, request, format=None):
        checklist = get_queryset(request, Checklist)
        serializer = ChecklistSerializer(checklist, many=True)
        return Response({'checklist': serializer.data})

    def post(self, request, format=None):
        serializer = ChecklistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
