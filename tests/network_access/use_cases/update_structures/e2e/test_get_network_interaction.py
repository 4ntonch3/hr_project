from apps.network_access.use_cases.update_structures.use_case import UpdateStructuresUseCase
from tests.conftest import ELTObjects, NetworkAccessObjects
from tests.custom_parametrize import parametrize_from_dict

get_network_interaction_cases = {
    'nothing_to_update': {
        'elt_objects': ELTObjects(),
        'network_access_objects': NetworkAccessObjects(),
        'expected_systems': [],
        'expected_stands': [],
    },
}


@parametrize_from_dict(get_network_interaction_cases)
def test_get_network_interaction_use_case_e2e(elt_objects, network_access_objects, expected_systems, expected_stands):
    use_case = UpdateStructuresUseCase()

    use_case.execute()
