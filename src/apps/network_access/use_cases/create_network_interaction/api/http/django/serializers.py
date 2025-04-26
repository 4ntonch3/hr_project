from rest_framework import serializers


class CreateNetworkInteractionRequestBodySerializer(serializers.Serializer):
    arch_interaction_guid = serializers.CharField(label='ID интеграции в Архитектурном Репозитории')
    src_arch_stand_guid = serializers.CharField(label='ID стенда источника в Архитектурном Репозитории')
    src_arch_component_guid = serializers.CharField(label='ID компонента источника в Архитектурном Репозитории')
    dst_arch_stand_guid = serializers.CharField(label='ID стенда назначения в Архитектурном Репозитории')
    dst_arch_component_guid = serializers.CharField(label='ID компонента назначения в Архитектурном Репозитории')
    src_network_zone_name = serializers.CharField(label='Название Сетевой Зоны источника')
    dst_network_zone_name = serializers.CharField(label='Название Сетевой Зоны назначения')
    protocol_to_ports = serializers.JSONField(label='Протоколы и порты взаимодействия')

    class Meta:
        ref_name = 'CreateNetworkInteractionRequestBody'


class CreateNetworkInteractionResponseBodySerializer(serializers.Serializer):
    id = serializers.CharField(label='ID Сетевого Взаимодействия')

    class Meta:
        ref_name = 'CreateNetworkInteractionResponseBody'
