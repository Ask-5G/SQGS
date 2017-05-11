from rest_framework import serializers

from basemodel.models import (Parts,
                              Models,
                              ModelParts,
                              )

from api.customfields import BinaryField


class PartsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parts
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class ModelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Models
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.sales_code = validated_data.get(
            'sales_code', instance.sales_code)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.base_sales_code = validated_data.get(
            'base_sales_code', instance.base_sales_code)
        instance.save()
        return instance


class ModelPartsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModelParts
        fields = "__all__"

    def update(self, instance, validated_data):

        instance.part_id = validated_data.get('part_id', instance.part_id)
        instance.model_id = validated_data.get('model_id', instance.model_id)
        instance.save()
        return instance
