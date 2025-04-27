from pydantic import BaseModel


class NetworkInteractionDTO(BaseModel):
    network_interaction_id: str
    src_access_group_id: str
    src_network_zone_name: str
    dst_access_group_id: str
    dst_network_zone_name: str
    is_activated: bool


class AccessGroupPrefixDTO(BaseModel):
    prefix: str
    is_activated: bool


class NetworkInteractionWithPrefixesDTO(BaseModel):
    network_interaction_id: str
    src_access_group_id: str
    src_network_zone_name: str
    src_prefixes: list[AccessGroupPrefixDTO]
    dst_access_group_id: str
    dst_network_zone_name: str
    dst_prefixes: list[AccessGroupPrefixDTO]
    is_activated: bool
