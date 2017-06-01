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
from reports.views import get_queryset


class PartsView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        parts = get_queryset(request, Parts)
        serializer = PartsSerializer(parts, many=True)
        return Response({'parts': serializer.data})
    

class ModelsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        models = get_queryset(request, Models)
        serializer = ModelsSerializer(models, many=True)
        return Response({'models': serializer.data})


class ModelPartsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        modelparts = get_queryset(request, ModelParts)
        serializer = ModelPartsSerializer(modelparts, many=True)
        return Response({'modelParts': serializer.data})




    


