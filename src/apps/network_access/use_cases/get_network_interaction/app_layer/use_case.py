from apps.network_access.use_cases.get_network_interaction.domain.repository_interface import (
    IGetNetworkInteractionRepository,
)
from apps.network_access.use_cases.get_network_interaction.dto import NetworkInteractionWithPrefixesDTO


class GetNetworkInteractionUseCase:
    def __init__(self, repo: IGetNetworkInteractionRepository) -> None:
        self._repo = repo

    def execute(self, ni_public_id: str) -> NetworkInteractionWithPrefixesDTO:
        with self._repo.transaction:
            ni = self._repo.get_network_interaction(ni_public_id)

            return NetworkInteractionWithPrefixesDTO(
                network_interaction_id=ni.network_interaction_id,
                src_access_group_id=ni.src_access_group_id,
                src_network_zone_name=ni.src_network_zone_name,
                src_prefixes=self._repo.get_access_group_prefixes(ni.src_access_group_id),
                dst_access_group_id=ni.dst_access_group_id,
                dst_network_zone_name=ni.dst_network_zone_name,
                dst_prefixes=self._repo.get_access_group_prefixes(ni.dst_access_group_id),
                is_activated=ni.is_activated,
            )
