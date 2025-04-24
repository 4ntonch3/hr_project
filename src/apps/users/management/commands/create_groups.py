from typing import Any

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand

from apps.users.groups import UserGroup
from apps.users.permissions import AccessOrchestratorPermission

_GET_MODEL = django_apps.get_model

_GROUP_AND_PERMISSIONS = [
    (
        UserGroup.ACCESS_ORCHESTRATOR_ADMIN,
        [AccessOrchestratorPermission.NetworkAccess.get_network_interaction],
    ),
    (
        UserGroup.STAND_ADMIN,
        [AccessOrchestratorPermission.NetworkAccess.get_network_interaction],
    ),
]


class Command(BaseCommand):
    help = "Create user groups with permissions"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        for role, permissions in _GROUP_AND_PERMISSIONS:
            permissions = [permission.split(".")[1] for permission in permissions]
            group_model = _GET_MODEL("auth", "Group")
            group, _ = group_model.objects.get_or_create(name=role)
            permissions = AccessOrchestratorPermission.object.filter(
                codename__in=permissions
            )
            group.permissions.add(*permissions)
