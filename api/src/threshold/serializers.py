from rest_framework import serializers
from threshold.models import Thresholds, ThresholdHistory, ThresholdNotifications

class ThresholdsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thresholds
        fields = ('name','no_of_occurances','duration','reset_upon_notification','inspection_point_defects_id')        
    
    def update(self, instance, validated_data):
        
        instance.name = validated_data.get('name', instance.name)
        instance.no_of_occurances = validated_data.get('no_of_occurances', instance.no_of_occurances)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.reset_upon_notification = validated_data.get('reset_upon_notification', instance.reset_upon_notification)
        instance.inspection_point_defects_id = validated_data.get('inspection_point_defects_id', instance.inspection_point_defects_id)
        instance.save()
        return instance   

class ThresholdHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ThresholdHistory
        fields = ('timestamp','threshold_id')   

    def update(self, instance, validated_data):
        
        instance.timestamp = validated_data.get('timestamp', instance.timestamp)
        instance.threshold_id = validated_data.get('threshold_id', instance.threshold_id)
        instance.save()
        return instance      

class ThresholdNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThresholdNotifications
        fields = ('role_id','user_id','threshold_id')                        

    def update(self, instance, validated_data):
        
        instance.role_id = validated_data.get('role_id', instance.role_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.threshold_id = validated_data.get('threshold_id', instance.threshold_id)
        instance.save()
        return instance      