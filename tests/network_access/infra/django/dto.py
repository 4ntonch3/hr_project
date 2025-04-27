from datetime import datetime
from ipaddress import IPv4Network

from pydantic import BaseModel


class NetworkZoneDTO(BaseModel):
    public_id: str
    name: str
    creation_reason: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PrefixDTO(BaseModel):
    public_id: str
    network_zone: str
    address: IPv4Network


class AccessGroupSourceDTO(BaseModel):
    public_id: str
    network_zones: list[str]
    arch_stand_guid: str
    arch_component_guid: str
    creation_reason: str
    unactual_at: datetime | None = None
    unactuality_reason: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AccessGroupDTO(BaseModel):
    name: str
    public_id: str
    source: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AccessGroup2PrefixDTO(BaseModel):
    public_id: str
    access_group_id: str
    prefix_id: str
    approver: str | None
    approved_at: datetime | None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NetworkInteractionSourceDTO(BaseModel):
    public_id: str
    src_network_zone: str
    dst_network_zone: str
    arch_interaction_guid: str
    creation_reason: str
    protocol_to_ports: str
    unactual_at: datetime | None = None
    unactuality_reason: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NetworkInteractionDTO(BaseModel):
    public_id: str
    source: str
    src_access_group: str
    dst_access_group: str
    creator: str

    activated_at: datetime | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
