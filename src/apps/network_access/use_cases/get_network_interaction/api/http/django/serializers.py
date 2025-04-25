from rest_framework import serializers


class GetNetworkInteractionPathSerializer(serializers.Serializer):
    network_interaction_id = serializers.UUIDField(label='ID СВ')


class GetNetworkInteractionResponseSerializer(serializers.Serializer):
    network_interaction_id = serializers.UUIDField(label='ID СВ')
    src_access_group_id = serializers.UUIDField(label='ID источика ГД')
    src_network_zone_name = serializers.CharField(label='Зона источник')
    dst_access_group_id = serializers.UUIDField(label='ID назначения ГД')
    dst_network_zone_name = serializers.CharField(label='Зона назначение')
    is_activated = serializers.BooleanField(label='СВ активировано?')
