from rest_framework import serializers


class BaseErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
    level = serializers.CharField(default='error')
