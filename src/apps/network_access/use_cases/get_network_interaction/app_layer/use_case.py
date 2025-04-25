from apps.network_access.use_cases.get_network_interaction.domain.repository_interface import (
    IGetNetworkInteractionRepository,
)
from apps.network_access.use_cases.get_network_interaction.dto import NetworkInteractionDTO


class GetNetworkInteractionUseCase:
    def __init__(self, repo: IGetNetworkInteractionRepository) -> None:
        self._repo = repo

    def execute(self, ni_public_id: str) -> NetworkInteractionDTO:
        return self._repo.get_network_interaction(ni_public_id)
