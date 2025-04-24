from rest_framework import serializers


class GetNetworkInteractionPathSerializer(serializers.Serializer):
    network_interaction_id = serializers.UUIDField(label="ID СВ")


class GetNetworkInteractionResponseSerializer(serializers.Serializer):
    name = serializers.CharField(label="Название СВ")
