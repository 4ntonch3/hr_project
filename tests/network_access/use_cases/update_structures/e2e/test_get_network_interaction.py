import pytest

from apps.elt.enum import ELTStatus, SystemType
from apps.network_access.models import Stand, System
from apps.network_access.use_cases.update_structures.use_case import UpdateStructuresUseCase
from tests.conftest import ELTObjects, NetworkAccessObjects
from tests.custom_parametrize import parametrize_from_dict
from tests.network_access.infra.django.dto import (
    ELTDeviceDTO,
    ELTStandDTO,
    ELTSystemDTO,
    ELTVersionDTO,
    StandDTO,
    SystemDTO,
)

# --- create_new_system_and_stand ---
_v1 = ELTVersionDTO(status=ELTStatus.ACTUAL)
_sys1 = ELTSystemDTO(ci='AS-001', system_type=SystemType.AS, name='System One', is_it_service=True, version=_v1)
_stand1 = ELTStandDTO(ci='STAND-001', name='Stand One', system=_sys1, version=_v1)

# --- update_existing_system_and_stand ---
_v2 = ELTVersionDTO(status=ELTStatus.ACTUAL)
_sys2_elt = ELTSystemDTO(ci='AS-002', system_type=SystemType.AS, name='Updated Name', is_it_service=False, version=_v2)
_stand2_elt = ELTStandDTO(ci='STAND-002', name='Updated Stand', system=_sys2_elt, version=_v2, sb_security_group='t')
_sys2_na = SystemDTO(ci='AS-002', name='Old Name', is_it_service=True, is_active=True)
_stand2_na = StandDTO(ci='STAND-002', name='Old Stand', has_anonymized_data=False, is_active=True, system=_sys2_na)

# --- deactivate_structures_missing_from_elt ---
_v3 = ELTVersionDTO(status=ELTStatus.ACTUAL)
_sys3_na = SystemDTO(ci='AS-003', name='Orphaned System', is_it_service=False, is_active=True)
_stand3_na = StandDTO(ci='STAND-003', name='Orphaned Stand', has_anonymized_data=False, is_active=True, system=_sys3_na)

# --- resolve_stand_ips_from_devices ---
_v4 = ELTVersionDTO(status=ELTStatus.ACTUAL)
_sys4 = ELTSystemDTO(ci='AS-004', system_type=SystemType.AS, name='IP System', is_it_service=False, version=_v4)
_dev4 = ELTDeviceDTO(ci='DEV-004', ips='192.168.1.0/24;10.0.0.0/8', version=_v4)
_stand4 = ELTStandDTO(ci='STAND-004', name='IP Stand', system=_sys4, version=_v4, devices='DEV-004')

# --- error_in_one_stand_does_not_stop_others ---
_v5 = ELTVersionDTO(status=ELTStatus.ACTUAL)
_sys5 = ELTSystemDTO(ci='AS-005', system_type=SystemType.AS, name='System Five', is_it_service=False, version=_v5)
_stand5_ok = ELTStandDTO(ci='STAND-005-OK', name='Good Stand', system=_sys5, version=_v5)
_stand5_fail = ELTStandDTO(ci='STAND-005-FAIL', name='Bad Stand', system=None, version=_v5)

get_network_interaction_cases = {
    'nothing_to_update': {
        'elt_objects': ELTObjects(),
        'network_access_objects': NetworkAccessObjects(),
        'expected_systems': [],
        'expected_stands': [],
    },
    'create_new_system_and_stand': {
        'elt_objects': ELTObjects(elt_versions=[_v1], elt_systems=[_sys1], elt_stands=[_stand1]),
        'network_access_objects': NetworkAccessObjects(),
        'expected_systems': [
            {'ci': 'AS-001', 'name': 'System One', 'is_it_service': True, 'is_active': True},
        ],
        'expected_stands': [
            {'ci': 'STAND-001', 'name': 'Stand One', 'is_active': True},
        ],
    },
    'update_existing_system_and_stand': {
        'elt_objects': ELTObjects(elt_versions=[_v2], elt_systems=[_sys2_elt], elt_stands=[_stand2_elt]),
        'network_access_objects': NetworkAccessObjects(systems=[_sys2_na], stands=[_stand2_na]),
        'expected_systems': [
            {'ci': 'AS-002', 'name': 'Updated Name', 'is_it_service': False, 'is_active': True},
        ],
        'expected_stands': [
            {'ci': 'STAND-002', 'name': 'Updated Stand', 'is_active': True},
        ],
    },
    'deactivate_structures_missing_from_elt': {
        'elt_objects': ELTObjects(elt_versions=[_v3]),
        'network_access_objects': NetworkAccessObjects(systems=[_sys3_na], stands=[_stand3_na]),
        'expected_systems': [
            {'ci': 'AS-003', 'name': 'Orphaned System', 'is_it_service': False, 'is_active': False},
        ],
        'expected_stands': [
            {'ci': 'STAND-003', 'name': 'Orphaned Stand', 'is_active': False},
        ],
    },
    'resolve_stand_ips_from_devices': {
        'elt_objects': ELTObjects(elt_versions=[_v4], elt_systems=[_sys4], elt_stands=[_stand4], elt_devices=[_dev4]),
        'network_access_objects': NetworkAccessObjects(),
        'expected_systems': [
            {'ci': 'AS-004', 'name': 'IP System', 'is_it_service': False, 'is_active': True},
        ],
        'expected_stands': [
            {'ci': 'STAND-004', 'name': 'IP Stand', 'is_active': True},
        ],
    },
    'error_in_one_stand_does_not_stop_others': {
        'elt_objects': ELTObjects(elt_versions=[_v5], elt_systems=[_sys5], elt_stands=[_stand5_ok, _stand5_fail]),
        'network_access_objects': NetworkAccessObjects(),
        'expected_systems': [
            {'ci': 'AS-005', 'name': 'System Five', 'is_it_service': False, 'is_active': True},
        ],
        'expected_stands': [
            {'ci': 'STAND-005-OK', 'name': 'Good Stand', 'is_active': True},
        ],
    },
}


@pytest.mark.django_db
@parametrize_from_dict(get_network_interaction_cases)
def test_get_network_interaction_use_case_e2e(
    init_elt_objects,
    init_network_access_objects,
    expected_systems: list[dict],
    expected_stands: list[dict],
) -> None:
    use_case = UpdateStructuresUseCase()

    use_case.execute()

    actual_systems = list(System.objects.values('ci', 'name', 'is_it_service', 'is_active').order_by('ci'))
    actual_stands = list(Stand.objects.values('ci', 'name', 'is_active').order_by('ci'))

    assert actual_systems == sorted(expected_systems, key=lambda x: x['ci'])
    assert actual_stands == sorted(expected_stands, key=lambda x: x['ci'])
