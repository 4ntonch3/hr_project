import json
from typing import ContextManager

from django.db import transaction as django_transaction

from apps.network_access.models.access_group import AccessGroup, AccessGroupSource
from apps.network_access.models.network_interaction import NetworkInteraction, NetworkInteractionSource
from apps.network_access.models.network_zone import NetworkZone
from apps.network_access.use_cases.create_network_interaction.domain.repository_interface import (
    ICreateNetworkInteractionRepository,
)


class CreateNetworkInteractionRepository(ICreateNetworkInteractionRepository):
    @property
    def transaction(self) -> ContextManager:
        return django_transaction.atomic()

    def get_network_zone_id_by_name(self, network_zones_names: list[str]) -> dict[str, int]:
        network_zones = NetworkZone.objects.filter(name__in=network_zones_names)

        return {network_zone.name: network_zone.pk for network_zone in network_zones}

    def create_access_group(
        self,
        arch_stand_guid: str,
        arch_component_guid: str,
        network_zone_id: int,
        creation_reason: str,
    ) -> int:
        source = AccessGroupSource.objects.create(
            arch_stand_guid=arch_stand_guid, arch_component_guid=arch_component_guid, creation_reason=creation_reason
        )
        source.network_zones.add(network_zone_id)
        source.save()

        ag = AccessGroup.objects.create(source=source.pk)

        return ag.pk

    def create_network_interaction(
        self,
        src_network_zone_id: int,
        dst_network_zone_id: int,
        src_access_group_id: int,
        dst_access_group_id: int,
        arch_interaction_guid: str,
        protocol_to_ports: dict[str, list[str]],
        creator_id: int,
        creation_reason: str,
    ) -> str:
        source = NetworkInteractionSource.objects.create(
            src_network_zone_id=src_network_zone_id,
            dst_network_zone_id=dst_network_zone_id,
            arch_interaction_guid=arch_interaction_guid,
            creation_reason=creation_reason,
            protocol_to_ports=json.dumps(protocol_to_ports),
        )

        ni = NetworkInteraction.objects.create(
            source=source.pk,
            src_access_group_id=src_access_group_id,
            dst_access_group_id=dst_access_group_id,
            creator_id=creator_id,
        )

        return ni.public_id
