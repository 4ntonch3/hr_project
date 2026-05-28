from apps.elt.models import ELTDevice, ELTStand, ELTSystem, FullELTVersion
from apps.network_access.models import Stand, System
from tests.network_access.infra.django.dto import (
    ELTDeviceDTO,
    ELTStandDTO,
    ELTSystemDTO,
    ELTVersionDTO,
    StandDTO,
    SystemDTO,
)


class CreateELTObjectsRepo:
    def __init__(self) -> None:
        self._version_map: dict[int, FullELTVersion] = {}
        self._system_map: dict[int, ELTSystem] = {}

    def create_elt_versions(self, versions: list[ELTVersionDTO]) -> None:
        for dto in versions:
            obj = FullELTVersion.objects.create(status=dto.status, info=dto.info)
            self._version_map[id(dto)] = obj

    def create_systems(self, systems: list[ELTSystemDTO]) -> None:
        for dto in systems:
            version = self._version_map.get(id(dto.version)) if dto.version else None
            obj = ELTSystem.objects.create(
                ci=dto.ci,
                system_type=dto.system_type,
                name=dto.name,
                status=dto.status,
                is_it_service=dto.is_it_service,
                version=version,
            )
            self._system_map[id(dto)] = obj

        for dto in systems:
            if dto.related_systems:
                obj = self._system_map[id(dto)]
                related = [self._system_map[id(r)] for r in dto.related_systems]
                obj.related_systems.set(related)

    def create_stands(self, stands: list[ELTStandDTO]) -> None:
        for dto in stands:
            version = self._version_map.get(id(dto.version)) if dto.version else None
            system = self._system_map.get(id(dto.system)) if dto.system else None
            ELTStand.objects.create(
                ci=dto.ci,
                sb_security_group=dto.sb_security_group,
                status=dto.status,
                name=dto.name,
                subtype=dto.subtype,
                devices=dto.devices,
                system=system,
                version=version,
            )

    def create_devices(self, devices: list[ELTDeviceDTO]) -> None:
        for dto in devices:
            version = self._version_map.get(id(dto.version)) if dto.version else None
            ELTDevice.objects.create(
                ci=dto.ci,
                type=dto.type,
                subtype=dto.subtype,
                name=dto.name,
                status=dto.status,
                ips=dto.ips,
                version=version,
            )


class CreateNetworkAccessObjectsRepo:
    def __init__(self) -> None:
        self._system_map: dict[int, System] = {}

    def create_systems(self, systems: list[SystemDTO]) -> None:
        for dto in systems:
            obj = System.objects.create(
                ci=dto.ci,
                name=dto.name,
                is_it_service=dto.is_it_service,
                is_active=dto.is_active,
            )
            self._system_map[id(dto)] = obj

    def create_stands(self, stands: list[StandDTO]) -> None:
        for dto in stands:
            system = self._system_map[id(dto.system)]
            Stand.objects.create(
                ci=dto.ci,
                name=dto.name,
                has_anonymized_data=dto.has_anonymized_data,
                ips=dto.ips,
                is_active=dto.is_active,
                system=system,
            )
