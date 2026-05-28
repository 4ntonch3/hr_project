from dataclasses import dataclass, field

import pytest

from tests.network_access.infra.django.dto import (
    ELTDeviceDTO,
    ELTStandDTO,
    ELTSystemDTO,
    ELTVersionDTO,
    StandDTO,
    SystemDTO,
)
from tests.network_access.infra.django.repo import CreateELTObjectsRepo, CreateNetworkAccessObjectsRepo


@dataclass
class ELTObjects:
    elt_versions: list[ELTVersionDTO] = field(default_factory=list)
    elt_systems: list[ELTSystemDTO] = field(default_factory=list)
    elt_stands: list[ELTStandDTO] = field(default_factory=list)
    elt_devices: list[ELTDeviceDTO] = field(default_factory=list)


@dataclass
class NetworkAccessObjects:
    systems: list[SystemDTO] = field(default_factory=list)
    stands: list[StandDTO] = field(default_factory=list)


@pytest.fixture(scope='function')
def elt_objects(elt_objects: ELTObjects) -> None:
    repo = CreateELTObjectsRepo()
    repo.create_elt_versions(elt_objects.elt_versions)
    repo.create_systems(elt_objects.elt_systems)
    repo.create_stands(elt_objects.elt_stands)
    repo.create_devices(elt_objects.elt_devices)


@pytest.fixture(scope='function')
def network_access_objects(network_access_objects: NetworkAccessObjects) -> None:
    repo = CreateNetworkAccessObjectsRepo()
    repo.create_systems(network_access_objects.systems)
    repo.create_stands(network_access_objects.stands)
