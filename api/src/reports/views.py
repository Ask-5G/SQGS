from django.shortcuts import render
from reports.models import *
from reports.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organization.authentication import SQGSTokenAuthentication
from dateutil import parser
from django.http import HttpResponseRedirect, HttpResponse

def get_image(request, pk):
    try:
        image = Images.objects.get(id=pk)
    except Images.DoesNotExist:
        return Response(
            {"error": "Images does not exist."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    if image.image:
        response = HttpResponse(image.image,
                                content_type='image/jpg',
                                status=200)
        response[
            'Content-Disposition'] = 'attachment; filename="%s"' % "{0}.jpg".format(image.description)
        return response
    else:
        return Response(
            {"error": "Image does not exist."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def get_queryset(request, myModel):
    try:
        date = request.GET.get('last_modified_date')
        if date != '':
            query = myModel.objects.filter(last_modified_date__gte=date)
        else:
            query = myModel.objects.all()   
        return query   
    except Exception as e:
        raise
    
class ReportsView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        serializer = ReportsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportScheduleView(APIView):
    
    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        serializer = ReportScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportDeliveryView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)
    
    def post(self, request, format=None):
        serializer = ReportDeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class PingRequestView(APIView):

    authentication_classes = (SQGSTokenAuthentication,)

    def post(self, request, format=None):
        updated_model_list = []
        updated_tables = UpdatedTables.objects.all().order_by('priority')
        if len(request.data) == 0:
            serializer = UpdatedTablesSerializer(updated_tables, many=True)
            return Response({'updated_tables': serializer.data}, status=status.HTTP_200_OK)
        else:
            for updated_table in updated_tables:
                table_name_found = False
                for requested_table in request.data:
                    if updated_table.name ==\
                            requested_table['name']:
                        table_name_found = True
                        request_date = parser.parse(
                            requested_table['last_modified_date'])
                        if updated_table.last_modified_date > request_date:
                            serializer = UpdatedTablesSerializer(updated_table)
                            updated_model_list.append(
                                serializer.data)
                        break
                if not table_name_found:
                    serializer = UpdatedTablesSerializer(updated_table)
                    updated_model_list.append(serializer.data)
        return Response({'updated_tables':updated_model_list}, status=status.HTTP_200_OK)               

class ImagesView(APIView):
   
    authentication_classes = (SQGSTokenAuthentication,)

    def get(self, request, format=None):
        images = get_queryset(request, Images)
        serializer = ImagesSerializer(images, many=True)
        return Response({'images': serializer.data})
    