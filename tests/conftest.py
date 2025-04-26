import pytest
from pydantic import BaseModel, Field

from tests.network_access.infra.django.dto import (
    AccessGroup2PrefixDTO,
    AccessGroupDTO,
    AccessGroupSourceDTO,
    NetworkInteractionDTO,
    NetworkInteractionSourceDTO,
    NetworkZoneDTO,
    PrefixDTO,
)
from tests.network_access.infra.django.repo import CreateNiEntitiesRepo


class NetworkInteractionConfig(BaseModel):
    network_zones: list[NetworkZoneDTO] = Field(default_factory=list)
    prefixes: list[PrefixDTO] = Field(default_factory=list)
    access_group_sources: list[AccessGroupSourceDTO] = Field(default_factory=list)
    access_groups: list[AccessGroupDTO] = Field(default_factory=list)
    access_groups_prefixes: list[AccessGroup2PrefixDTO] = Field(default_factory=list)
    network_interaction_sources: list[NetworkInteractionSourceDTO] = Field(default_factory=list)
    network_interactions: list[NetworkInteractionDTO] = Field(default_factory=list)


@pytest.fixture(scope='function')
def network_interaction_entities(ni_entities_config: NetworkInteractionConfig) -> None:
    repo = CreateNiEntitiesRepo()
    repo.create_network_zones(ni_entities_config.network_zones)
    repo.create_prefixes(ni_entities_config.prefixes)
    repo.create_access_group_sources(ni_entities_config.access_group_sources)
    repo.create_access_groups(ni_entities_config.access_groups)
    repo.create_access_groups_prefixes(ni_entities_config.access_groups_prefixes)
    repo.create_network_interaction_sources(ni_entities_config.network_interaction_sources)
    repo.create_network_interactions(ni_entities_config.network_interactions)
