from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from organization.models import (Plants,
                                 Cells,
                                 Shifts,
                                 Stages,
                                 ModelStations,
                                 Stations,
                                 UpdatedTables,
                                 Roles,
                                 Users,
                                 VerificationLog,
                                 SkillLevel,
                                 StageUser,
                                 DefectCategories,
                                 SourceGates)
from organization.authentication import SQGSAuthentication

from api.customfields import BinaryField


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        style={'input_type': 'password'}, required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = SQGSAuthentication().authenticate(
            username, password)
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)
            elif user.is_expired:
                user.generate_key()
                user.calculate_new_expiration()
                user.save(
                    update_fields=['key', 'key_expiry_date'])
        else:
            msg = _('Unable to log in with provided credentials')
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class VerificationLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationLog
        fields = "__all__"  


class UpdatedTablesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdatedTables
        fields = ('name', 'last_modified_date')


class PlantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plants
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.plant_name = validated_data.get(
            'plant_name', instance.plant_name)
        instance.save()
        return instance


class CellsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cells
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.description = validated_data.get(
            'description', instance.description)
        instance.plants = validated_data.get('plants', instance.plants)
        instance.save()
        return instance


class StagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stages
        fields = "__all__"


class ModelStationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelStations
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.image = validated_data.get('image', instance.image)
        instance.model_id = validated_data.get('model_id', instance.model_id)
        instance.station_id = validated_data.get(
            'station_id', instance.station_id)
        instance.side = validated_data.get('side', instance.side)
        instance.save()
        return instance


class StationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stations
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.description = validated_data.get(
            'description', instance.description)
        instance.cells = validated_data.get('cells', instance.cells)
        instance.save()
        return instance


class ShiftsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shifts
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.start_time = validated_data.get(
            'start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.plants = validated_data.get('plants', instance.plants)
        instance.save()
        return instance


class RolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class SkillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevel
        fields = "__all__"

class StageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageUser
        fields = "__all__"

class DefectCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectCategories
        fields = "__all__"

class SourceGatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceGates
        fields = "__all__"

