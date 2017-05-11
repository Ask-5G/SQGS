from rest_framework import serializers

from checkpoints.models import (
                                Defects,
                                InspectionTypes, 
                                PartDefects, 
                                Repairs, 
                                Checkpoints,
                                CheckpointDefects,
                                Checklist)


class DefectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Defects
        fields = "__all__"

    def update(self, instance, validated_data):
        
        instance.description = validated_data.get('description', instance.description)
        instance.defect_category_id = validated_data.get('defect_category_id', instance.defect_category_id)
        instance.save()
        return instance


class PartDefectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartDefects
        fields = "__all__"   

    def update(self, instance, validated_data):
        
        instance.modelpart_id = validated_data.get('modelpart_id', instance.modelpart_id)
        instance.defect_id = validated_data.get('defect_id', instance.defect_id)
        instance.save()
        return instance

class RepairsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repairs 
        fields = "__all__"  

    def update(self, instance, validated_data):
        
        instance.description = validated_data.get('description', instance.description)
        instance.defect_id = validated_data.get('defect_id', instance.defect_id)
        instance.save()
        return instance 

class CheckpointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checkpoints
        fields = "__all__"

    def update(self, instance, validated_data):
        
        instance.station_id = validated_data.get('station_id', instance.station_id)
        instance.description = validated_data.get('description', instance.description)
        instance.inspection_types = validated_data.get('inspection_types', instance.inspection_types)
        instance.save()
        return instance

class CheckpointDefectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckpointDefects
        fields = "__all__"

    def update(self, instance, validated_data):
        
        instance.station_id = validated_data.get('station_id', instance.station_id)
        instance.description = validated_data.get('description', instance.description)
        instance.inspection_types = validated_data.get('inspection_types', instance.inspection_types)
        instance.save()
        return instance

class InspectionTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = InspectionTypes
        fields = "__all__"

    def update(self, instance, validated_data):
        
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class ChecklistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checklist
        fields = "__all__"