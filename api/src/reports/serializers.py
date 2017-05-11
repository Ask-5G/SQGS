from rest_framework import serializers

from reports.models import *

class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = ('name')

    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance        

class ReportScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportSchedule
        fields = ('hour','day','month','shift','week','reports')

    def update(self, instance, validated_data):
        
        instance.hour = validated_data.get('hour', instance.hour)
        instance.day = validated_data.get('day', instance.day)
        instance.month = validated_data.get('month', instance.month)
        instance.shift = validated_data.get('shift', instance.shift)
        instance.week = validated_data.get('week', instance.week)
        instance.reports = validated_data.get('reports', instance.reports)
        instance.save()
        return instance   

class ReportDeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportDelivery
        fields = ('user_id','role_id','report_schedule')  

    def update(self, instance, validated_data):
        
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.role_id = validated_data.get('role_id', instance.role_id)
        instance.report_schedule = validated_data.get('report_schedule', instance.report_schedule)
        instance.save()
        return instance 

class UpdatedTablesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdatedTables
        fields = ('name','last_modified_date')

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = "__all__"