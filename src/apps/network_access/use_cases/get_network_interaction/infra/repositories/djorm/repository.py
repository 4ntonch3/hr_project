from typing import ContextManager

from django.db import transaction as django_transaction

from apps.network_access.models.access_group import AccessGroup2Prefix
from apps.network_access.models.network_interaction import NetworkInteraction
from apps.network_access.use_cases.get_network_interaction.domain.exceptions import (
    NetworkInteractionNotFoundError,
)
from apps.network_access.use_cases.get_network_interaction.domain.repository_interface import (
    IGetNetworkInteractionRepository,
)
from apps.network_access.use_cases.get_network_interaction.dto import (
    AccessGroupPrefixDTO,
    NetworkInteractionDTO,
)


class GetNetworkInteractionRepository(IGetNetworkInteractionRepository):
    @property
    def transaction(self) -> ContextManager:
        return django_transaction.atomic()

    def get_network_interaction(self, ni_public_id: str) -> NetworkInteractionDTO:
        try:
            ni = NetworkInteraction.objects.get(public_id=ni_public_id)
        except NetworkInteraction.DoesNotExist:
            raise NetworkInteractionNotFoundError(f'Сетевое взаимодействие с id {ni_public_id} не найдено')

        return NetworkInteractionDTO(
            network_interaction_id=ni.public_id,
            src_access_group_id=ni.src_access_group.public_id,
            src_network_zone_name=ni.source.src_network_zone.name,
            dst_access_group_id=ni.dst_access_group.public_id,
            dst_network_zone_name=ni.source.dst_network_zone.name,
            is_activated=bool(ni.activated_at),
        )

    def get_access_group_prefixes(self, access_group_id: str) -> list[AccessGroupPrefixDTO]:
        return [
            AccessGroupPrefixDTO(
                prefix=str(relation.prefix.address),
                is_activated=bool(relation.approved_at),
            )
            for relation in AccessGroup2Prefix.objects.filter(access_group__public_id=access_group_id).select_related(
                'prefix'
            )
        ]
