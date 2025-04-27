from apps.network_access.models.access_group import AccessGroup, AccessGroup2Prefix, AccessGroupSource
from apps.network_access.models.network_interaction import NetworkInteraction, NetworkInteractionSource
from apps.network_access.models.network_zone import NetworkZone
from apps.network_access.models.prefix import Prefix
from apps.users.models import User
from tests.network_access.infra.django.dto import (
    AccessGroup2PrefixDTO,
    AccessGroupDTO,
    AccessGroupSourceDTO,
    NetworkInteractionDTO,
    NetworkInteractionSourceDTO,
    NetworkZoneDTO,
    PrefixDTO,
)


class CreateNiEntitiesRepo:
    def create_network_zones(self, zones: list[NetworkZoneDTO]) -> None:
        zones_obj = []
        for zone in zones:
            zone_obj = NetworkZone(
                public_id=zone.public_id,
                name=zone.name,
                creation_reason=zone.creation_reason,
            )
            if zone.created_at:
                zone_obj.created_at = zone.created_at
            if zone.updated_at:
                zone_obj.updated_at = zone.updated_at
            zones_obj.append(zone_obj)

        NetworkZone.objects.bulk_create(zones_obj)

    def create_prefixes(self, prefixes: list[PrefixDTO]) -> None:
        prefixes_obj = []
        for prefix in prefixes:
            prefix_obj = Prefix(
                public_id=prefix.public_id,
                network_zone=NetworkZone.objects.get(public_id=prefix.network_zone),
                address=prefix.address,
            )
            prefixes_obj.append(prefix_obj)
        Prefix.objects.bulk_create(prefixes_obj)

    def create_access_group_sources(self, access_group_sources: list[AccessGroupSourceDTO]) -> None:
        for source in access_group_sources:
            source_obj = AccessGroupSource.objects.create(
                public_id=source.public_id,
                arch_stand_guid=source.arch_stand_guid,
                arch_component_guid=source.arch_component_guid,
                creation_reason=source.creation_reason,
            )
            if source.unactual_at:
                source_obj.unactual_at = source.unactual_at
            if source.created_at:
                source_obj.created_at = source.created_at
            if source.updated_at:
                source_obj.updated_at = source.updated_at
            if source.unactuality_reason:
                source_obj.unactuality_reason = source.unactuality_reason
            source_obj.save()
            zones = NetworkZone.objects.filter(public_id__in=source.network_zones)
            source_obj.network_zones.set(zones)

    def create_access_groups(self, access_groups: list[AccessGroupDTO]) -> None:
        groups_obj = []
        for group in access_groups:
            group_obj = AccessGroup(
                public_id=group.public_id,
                name=group.name,
                source=AccessGroupSource.objects.get(public_id=group.source),
            )
            if group.updated_at:
                group_obj.updated_at = group.updated_at
            if group.created_at:
                group_obj.created_at = group.created_at
            groups_obj.append(group_obj)
        AccessGroup.objects.bulk_create(groups_obj)

    def create_access_groups_prefixes(self, access_groups_prefixes: list[AccessGroup2PrefixDTO]) -> None:
        records_obj = []
        for record in access_groups_prefixes:
            approver = None
            if record.approver:
                approver, _ = User.objects.get_or_create(username=record.approver)
            record_obj = AccessGroup2Prefix(
                public_id=record.public_id,
                access_group=AccessGroup.objects.get(public_id=record.access_group_id),
                prefix=Prefix.objects.get(public_id=record.prefix_id),
                approver=approver,
                approved_at=record.approved_at,
            )
            if record.created_at:
                record_obj.created_at = record.created_at
            if record.updated_at:
                record_obj.updated_at = record.updated_at
            records_obj.append(record_obj)
        AccessGroup2Prefix.objects.bulk_create(records_obj)

    def create_network_interaction_sources(self, sources: list[NetworkInteractionSourceDTO]) -> None:
        sources_obj = []
        for source in sources:
            source_obj = NetworkInteractionSource(
                public_id=source.public_id,
                src_network_zone=NetworkZone.objects.get(public_id=source.src_network_zone),
                dst_network_zone=NetworkZone.objects.get(public_id=source.dst_network_zone),
                arch_interaction_guid=source.arch_interaction_guid,
                creation_reason=source.creation_reason,
                protocol_to_ports=source.protocol_to_ports,
            )
            if source.unactual_at:
                source_obj.unactual_at = source.unactual_at
            if source.created_at:
                source_obj.created_at = source.created_at
            if source.updated_at:
                source_obj.updated_at = source.updated_at
            if source.unactuality_reason:
                source_obj.unactuality_reason = source.unactuality_reason
            sources_obj.append(source_obj)
        NetworkInteractionSource.objects.bulk_create(sources_obj)

    def create_network_interactions(self, network_interactions: list[NetworkInteractionDTO]) -> None:
        interactions_obj = []
        for interaction in network_interactions:
            creator, _ = User.objects.get_or_create(username=interaction.creator)
            interaction_obj = NetworkInteraction(
                public_id=interaction.public_id,
                source=NetworkInteractionSource.objects.get(public_id=interaction.source),
                src_access_group=AccessGroup.objects.get(public_id=interaction.src_access_group),
                dst_access_group=AccessGroup.objects.get(public_id=interaction.dst_access_group),
                creator=creator,
                activated_at=interaction.activated_at,
            )
            if interaction.created_at:
                interaction_obj.created_at = interaction.created_at
            if interaction.updated_at:
                interaction_obj.updated_at = interaction.updated_at
            interactions_obj.append(interaction_obj)
        NetworkInteraction.objects.bulk_create(interactions_obj)
