from rest_framework import serializers
from inspection.models import InspectionDefects, DefectClosure, VinDetails, Verification, FinalRFT
from reports.models import *

class VinDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VinDetails
        fields = "__all__"  

    def update(self, instance, validated_data):   
        instance.vin = validated_data.get('vin', instance.vin)
        instance.model_id = validated_data.get('model_id', instance.model_id)
        instance.users_id = validated_data.get('users_id', instance.users_id)
        instance.stations_id = validated_data.get('stations_id', instance.stations_id)
        instance.shift_id = validated_data.get('shift_id', instance.shift_id)
        instance.save()
        return instance

class InspectionDefectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InspectionDefects
        fields = "__all__"


class DefectClosureSerializer(serializers.ModelSerializer):

    class Meta:
        model = DefectClosure
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.created_time = validated_data.get('created_time', instance.created_time)
        instance.updated_time = validated_data.get('updated_time', instance.updated_time)
        instance.repair_id = validated_data.get('repair_id', instance.repair_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)        
        instance.inspection_defect_id = validated_data.get('inspection_defect_id', instance.inspection_defect_id)
        instance.save()
        return instance

 
class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Verification
        fields = "__all__"

class FinalRFTSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinalRFT
        fields = "__all__"          