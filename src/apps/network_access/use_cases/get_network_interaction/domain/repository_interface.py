from abc import ABC, abstractmethod
from typing import ContextManager

from apps.network_access.use_cases.get_network_interaction.dto import (
    NetworkInteractionDTO,
)


class IGetNetworkInteractionRepository(ABC):
    @property
    @abstractmethod
    def transaction(self) -> ContextManager:
        pass

    @abstractmethod
    def get_network_interaction(self, ni_public_id: str) -> NetworkInteractionDTO:
        pass
