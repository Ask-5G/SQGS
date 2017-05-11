from rest_framework import serializers


class BinaryField(serializers.Field):

    def to_representation(self, value):
        """
        Convert our single email value to a list compliying with SCIM
        """
        return value
