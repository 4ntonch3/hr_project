from typing import ContextManager

from django.db import transaction as django_transaction

from apps.network_access.models.network_interaction import NetworkInteraction
from apps.network_access.use_cases.get_network_interaction.domain.exceptions import (
    NetworkInteractionNotFoundError,
)
from apps.network_access.use_cases.get_network_interaction.domain.repository_interface import (
    IGetNetworkInteractionRepository,
)
from apps.network_access.use_cases.get_network_interaction.dto import (
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
            public_id=ni.public_id,
            src_access_group_id=ni.src_access_group.public_id,
            src_network_zone_name=ni.source.src_network_zone.name,
            dst_access_group_id=ni.dst_access_group.public_id,
            dst_network_zone_name=ni.source.dst_network_zone.name,
            is_activated=bool(ni.activated_at),
        )
