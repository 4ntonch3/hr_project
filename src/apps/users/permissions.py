from enum import StrEnum

from django.contrib.auth.models import Permission
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class AccessOrchestratorPermission(Permission):
    class NetworkAccess(StrEnum):
        get_network_interaction = 'users.get_network_interaction'
        create_network_interaction = 'users.create_network_interaction'

    class Meta:
        proxy = True
        permissions = [
            (
                'users.get_network_interaction',
                'Могу получить Сетевое Взаимодействие',
            ),
            (
                'users.create_network_interaction',
                'Могу создать Сетевое Взаимодействие',
            ),
        ]


class SimpleUserPermission(BasePermission):
    @staticmethod
    def get_permission_required(view: ViewSet, action: str) -> tuple:
        if isinstance(view.permission_required, str):
            return (view.permission_required,)

        raw_perms = view.permission_required.get(action)
        if raw_perms is None:
            return ()

        if isinstance(raw_perms, str):
            return (raw_perms,)

        return raw_perms

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        perms = self.get_permission_required(view, view.action)
        if perms:
            return request.user.has_perms(perms)
        return True


class PermissionRequiredMixin:
    permission_required: dict[str, list[str]] | None = None
    permission_classes = [IsAuthenticated, SimpleUserPermission]
