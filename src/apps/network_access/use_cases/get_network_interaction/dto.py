from pydantic import BaseModel


class NetworkInteractionDTO(BaseModel):
    network_interaction_id: str
    src_access_group_id: str
    src_network_zone_name: str
    dst_access_group_id: str
    dst_network_zone_name: str
    is_activated: bool
