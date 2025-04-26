from abc import ABC, abstractmethod
from typing import ContextManager


class ICreateNetworkInteractionRepository(ABC):
    @property
    @abstractmethod
    def transaction(self) -> ContextManager:
        pass

    @abstractmethod
    def get_network_zone_id_by_name(self, network_zones_names: list[str]) -> dict[str, int]:
        pass

    @abstractmethod
    def create_access_group(
        self,
        arch_stand_guid: str,
        arch_component_guid: str,
        network_zone_id: int,
        creation_reason: str,
    ) -> str:
        pass

    @abstractmethod
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
        pass
