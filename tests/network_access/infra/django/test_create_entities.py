import uuid
from datetime import datetime
from ipaddress import IPv4Network

import pytest

from apps.network_access.models.access_group import AccessGroup, AccessGroup2Prefix, AccessGroupSource
from apps.network_access.models.network_interaction import NetworkInteraction, NetworkInteractionSource
from apps.network_access.models.network_zone import NetworkZone
from apps.network_access.models.prefix import Prefix
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
    name='eAZ',
    creation_reason='creation reason',
)
zone_2 = NetworkZoneDTO(
    public_id=str(uuid.uuid4()),
    name='eBZ',
    creation_reason='creation reason',
)
prefix_1 = PrefixDTO(
    public_id=str(uuid.uuid4()),
    network_zone=zone_1.public_id,
    address=IPv4Network('192.168.0.0/24'),
)
prefix_2 = PrefixDTO(
    public_id=str(uuid.uuid4()),
    network_zone=zone_2.public_id,
    address=IPv4Network('192.168.1.0/24'),
)
ag_source_1 = AccessGroupSourceDTO(
    public_id=str(uuid.uuid4()),
    network_zones=[zone_1.public_id],
    arch_stand_guid=str(uuid.uuid4()),
    arch_component_guid=str(uuid.uuid4()),
    creation_reason='creation_reason',
)
ag_source_2 = AccessGroupSourceDTO(
    public_id=str(uuid.uuid4()),
    network_zones=[zone_2.public_id],
    arch_stand_guid=str(uuid.uuid4()),
    arch_component_guid=str(uuid.uuid4()),
    creation_reason='creation_reason',
)
ag_1 = AccessGroupDTO(
    public_id=str(uuid.uuid4()),
    name='ag_1',
    source=ag_source_1.public_id,
)
ag_2 = AccessGroupDTO(
    public_id=str(uuid.uuid4()),
    name='ag_2',
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
    creation_reason='creation_reason',
    protocol_to_ports='{"TCP":["43","443"],"UDP":["444"]}',
    unactual_at=datetime.now(),
    unactuality_reason='unactuality_reason',
)
ni_source_2 = NetworkInteractionSourceDTO(
    public_id=str(uuid.uuid4()),
    src_network_zone=zone_2.public_id,
    dst_network_zone=zone_1.public_id,
    arch_interaction_guid=str(uuid.uuid4()),
    creation_reason='creation_reason',
    protocol_to_ports='{"TCP":["43","443"],"UDP":["444"]}',
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


cases = {
    'test_create_entities': {
        'ni_entities_config': NetworkInteractionConfig(
            network_zones=[zone_1, zone_2],
            prefixes=[prefix_1, prefix_2],
            access_group_sources=[ag_source_1, ag_source_2],
            access_groups=[ag_1, ag_2],
            access_groups_prefixes=[ag2prefix_1, ag2prefix_2],
            network_interaction_sources=[ni_source_1, ni_source_2],
            network_interactions=[ni_1, ni_2],
        )
    }
}


@parametrize_from_dict(cases)
@pytest.mark.django_db
def test_create_entities(network_interaction_entities):
    assert AccessGroup.objects.exists()
    assert AccessGroup2Prefix.objects.exists()
    assert AccessGroupSource.objects.exists()
    assert NetworkInteraction.objects.exists()
    assert NetworkInteractionSource.objects.exists()
    assert NetworkZone.objects.exists()
    assert Prefix.objects.exists()
