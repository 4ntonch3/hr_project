import uuid
from contextlib import nullcontext
from datetime import datetime
from ipaddress import IPv4Network

import pytest

from apps.network_access.use_cases.get_network_interaction.app_layer.use_case import (
    GetNetworkInteractionUseCase,
)
from apps.network_access.use_cases.get_network_interaction.domain.exceptions import (
    NetworkInteractionNotFoundError,
)
from apps.network_access.use_cases.get_network_interaction.dto import (
    AccessGroupPrefixDTO,
    NetworkInteractionWithPrefixesDTO,
)
from apps.network_access.use_cases.get_network_interaction.infra.repositories.djorm.repository import (
    GetNetworkInteractionRepository,
)
from tests.conftest import NetworkInteractionConfig
from tests.custom_parametrize import parametrize_from_dict
from tests.network_access.infra.django.dto import (
    AccessGroup2PrefixDTO,
    AccessGroupDTO,
    AccessGroupSourceDTO,
    NetworkInteractionDTO,
    NetworkInteractionSourceDTO,
    NetworkZoneDTO,
    PrefixDTO,
)

zone_1 = NetworkZoneDTO(
    public_id=str(uuid.uuid4()),
    name='TestZoneA',
    creation_reason='test reason',
)
zone_2 = NetworkZoneDTO(
    public_id=str(uuid.uuid4()),
    name='TestZoneB',
    creation_reason='test reason',
)
prefix_1 = PrefixDTO(
    public_id=str(uuid.uuid4()),
    network_zone=zone_1.public_id,
    address=IPv4Network('10.0.0.0/24'),
)
prefix_2 = PrefixDTO(
    public_id=str(uuid.uuid4()),
    network_zone=zone_2.public_id,
    address=IPv4Network('10.0.1.0/24'),
)
ag_source_1 = AccessGroupSourceDTO(
    public_id=str(uuid.uuid4()),
    network_zones=[zone_1.public_id],
    arch_stand_guid=str(uuid.uuid4()),
    arch_component_guid=str(uuid.uuid4()),
    creation_reason='test reason',
)
ag_source_2 = AccessGroupSourceDTO(
    public_id=str(uuid.uuid4()),
    network_zones=[zone_2.public_id],
    arch_stand_guid=str(uuid.uuid4()),
    arch_component_guid=str(uuid.uuid4()),
    creation_reason='test reason',
)
ag_1 = AccessGroupDTO(
    public_id=str(uuid.uuid4()),
    name='TestAG1',
    source=ag_source_1.public_id,
)
ag_2 = AccessGroupDTO(
    public_id=str(uuid.uuid4()),
    name='TestAG2',
    source=ag_source_2.public_id,
)
ag2prefix_1 = AccessGroup2PrefixDTO(
    public_id=str(uuid.uuid4()),
    access_group_id=ag_1.public_id,
    prefix_id=prefix_1.public_id,
    approver='approver',
    approved_at=datetime.now(),
)
ag2prefix_2 = AccessGroup2PrefixDTO(
    public_id=str(uuid.uuid4()),
    access_group_id=ag_2.public_id,
    prefix_id=prefix_2.public_id,
    approver=None,
    approved_at=None,
)
ni_source_1 = NetworkInteractionSourceDTO(
    public_id=str(uuid.uuid4()),
    src_network_zone=zone_1.public_id,
    dst_network_zone=zone_2.public_id,
    arch_interaction_guid=str(uuid.uuid4()),
    creation_reason='test reason',
    protocol_to_ports='{"TCP":["80"],"UDP":["53"]}',
    unactual_at=datetime.now(),
    unactuality_reason='test',
)
ni_source_2 = NetworkInteractionSourceDTO(
    public_id=str(uuid.uuid4()),
    src_network_zone=zone_2.public_id,
    dst_network_zone=zone_1.public_id,
    arch_interaction_guid=str(uuid.uuid4()),
    creation_reason='test reason',
    protocol_to_ports='{"TCP":["80"],"UDP":["53"]}',
)
ni_1 = NetworkInteractionDTO(
    public_id=str(uuid.uuid4()),
    source=ni_source_1.public_id,
    src_access_group=ag_1.public_id,
    dst_access_group=ag_2.public_id,
    creator='creator',
    activated_at=datetime.now(),
)
ni_2 = NetworkInteractionDTO(
    public_id=str(uuid.uuid4()),
    source=ni_source_2.public_id,
    src_access_group=ag_2.public_id,
    dst_access_group=ag_1.public_id,
    creator='creator',
    activated_at=None,
)

ni_entities_config = NetworkInteractionConfig(
    network_zones=[zone_1, zone_2],
    prefixes=[prefix_1, prefix_2],
    access_group_sources=[ag_source_1, ag_source_2],
    access_groups=[ag_1, ag_2],
    access_groups_prefixes=[ag2prefix_1, ag2prefix_2],
    network_interaction_sources=[ni_source_1, ni_source_2],
    network_interactions=[ni_1, ni_2],
)

get_network_interaction_cases = {
    'activated_interaction': {
        'ni_entities_config': ni_entities_config,
        'public_id': ni_1.public_id,
        'expected': NetworkInteractionWithPrefixesDTO(
            network_interaction_id=ni_1.public_id,
            src_access_group_id=ni_1.src_access_group,
            dst_access_group_id=ni_1.dst_access_group,
            src_network_zone_name=zone_1.name,
            dst_network_zone_name=zone_2.name,
            src_prefixes=[
                AccessGroupPrefixDTO(
                    prefix=str(prefix_1.address),
                    is_activated=True,
                )
            ],
            dst_prefixes=[
                AccessGroupPrefixDTO(
                    prefix=str(prefix_2.address),
                    is_activated=False,
                )
            ],
            is_activated=True,
        ),
        'expected_context': nullcontext(),
    },
    'not_activated_interaction': {
        'ni_entities_config': ni_entities_config,
        'public_id': ni_2.public_id,
        'expected': NetworkInteractionWithPrefixesDTO(
            network_interaction_id=ni_2.public_id,
            src_access_group_id=ni_2.src_access_group,
            dst_access_group_id=ni_2.dst_access_group,
            src_network_zone_name=zone_2.name,
            dst_network_zone_name=zone_1.name,
            src_prefixes=[
                AccessGroupPrefixDTO(
                    prefix=str(prefix_2.address),
                    is_activated=False,
                )
            ],
            dst_prefixes=[
                AccessGroupPrefixDTO(
                    prefix=str(prefix_1.address),
                    is_activated=True,
                )
            ],
            is_activated=False,
        ),
        'expected_context': nullcontext(),
    },
    'not_found_interaction': {
        'ni_entities_config': ni_entities_config,
        'public_id': str(uuid.uuid4()),  # Non-existent network interaction ID
        'expected': None,
        'expected_context': pytest.raises(NetworkInteractionNotFoundError),
    },
}


@parametrize_from_dict(get_network_interaction_cases)
@pytest.mark.django_db
def test_get_network_interaction_use_case_e2e(
    ni_entities_config, public_id, expected, expected_context, network_interaction_entities
):
    repo = GetNetworkInteractionRepository()
    use_case = GetNetworkInteractionUseCase(repo)

    with expected_context:
        result = use_case.execute(public_id)
        assert result == expected
