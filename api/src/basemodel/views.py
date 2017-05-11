from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from basemodel.models  import (Parts, 
                            Models, 
                            ModelParts, 
                              )

from basemodel.serializers import (PartsSerializer,
                                ModelsSerializer,
                                ModelPartsSerializer,  
                                )
from organization.authentication import SQGSTokenAuthentication
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view
from django.http import HttpResponse


class PartsView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            parts = Parts.objects.filter(last_modified_date__gte=date)
        else:
            parts = Parts.objects.all()
        serializer = PartsSerializer(parts, many=True)
        print serializer.data
        return Response({'parts': serializer.data})
    

class ModelsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        date = request.GET.get('last_modified_date')
        if date != '':
            models = Models.objects.filter(last_modified_date__gte=date)
        else:
            models = Models.objects.all()
        serializer = ModelsSerializer(models, many=True)
        return Response({'models': serializer.data})


class ModelPartsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        modelparts = ModelParts.objects.all()
        serializer = ModelPartsSerializer(modelparts, many=True)
        return Response({'modelParts': serializer.data})




    


