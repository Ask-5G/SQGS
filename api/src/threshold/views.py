from django.shortcuts import render
from threshold.models import Thresholds, ThresholdHistory, ThresholdNotifications
from threshold.serializers import ThresholdsSerializer, ThresholdHistorySerializer, ThresholdNotificationSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organization.authentication import SQGSTokenAuthentication


class ThresholdsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        serializer = ThresholdsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThresholdHistoryView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        serializer = ThresholdHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThresholdNotificationView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        serializer = ThresholdNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                