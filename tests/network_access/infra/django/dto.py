from dataclasses import dataclass, field

from apps.elt.enum import ELTStatus, SystemType


@dataclass
class ELTVersionDTO:
    status: ELTStatus
    info: dict | None = None


@dataclass
class ELTSystemDTO:
    ci: str
    system_type: SystemType
    name: str
    status: str | None = None
    is_it_service: bool | None = None
    version: ELTVersionDTO | None = None
    related_systems: list['ELTSystemDTO'] = field(default_factory=list)


@dataclass
class ELTStandDTO:
    ci: str
    system: ELTSystemDTO | None = None
    version: ELTVersionDTO | None = None
    sb_security_group: str | None = None
    status: str | None = None
    name: str | None = None
    subtype: str | None = None
    devices: str | None = None


@dataclass
class ELTDeviceDTO:
    ci: str
    version: ELTVersionDTO | None = None
    type: str | None = None
    subtype: str | None = None
    name: str | None = None
    status: str | None = None
    ips: str | None = None


@dataclass
class SystemDTO:
    ci: str
    name: str
    is_it_service: bool
    is_active: bool


@dataclass
class StandDTO:
    ci: str
    name: str
    has_anonymized_data: bool
    is_active: bool
    system: SystemDTO
    ips: list[str] = field(default_factory=list)
