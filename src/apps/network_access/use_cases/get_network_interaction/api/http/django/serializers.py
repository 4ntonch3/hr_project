from rest_framework import serializers


class GetNetworkInteractionPathSerializer(serializers.Serializer):
    network_interaction_id = serializers.UUIDField(label='ID СВ')


class AccessGroupPrefixSerializer(serializers.Serializer):
    prefix = serializers.CharField(label='Префикс')
    is_activated = serializers.BooleanField(label='Префикс активирован?')

    class Meta:
        ref_name = 'AccessGroupPrefix'


class GetNetworkInteractionResponseBodySerializer(serializers.Serializer):
    network_interaction_id = serializers.UUIDField(label='ID СВ')
    src_access_group_id = serializers.UUIDField(label='ID источика ГД')
    src_network_zone_name = serializers.CharField(label='Зона источник')
    src_prefixes = AccessGroupPrefixSerializer(many=True, label='Префиксы источника')
    dst_access_group_id = serializers.UUIDField(label='ID назначения ГД')
    dst_network_zone_name = serializers.CharField(label='Зона назначение')
    dst_prefixes = AccessGroupPrefixSerializer(many=True, label='Префиксы назначения')
    is_activated = serializers.BooleanField(label='СВ активировано?')

    class Meta:
        ref_name = 'GetNetworkInteractionResponseBody'
