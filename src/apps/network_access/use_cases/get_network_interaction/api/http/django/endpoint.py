import logging
from http import HTTPStatus

from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.serializers import BaseErrorSerializer
from apps.users.permissions import AccessOrchestratorPermission, PermissionRequiredMixin

from .openapi_doc import get_network_interaction_doc
from .serializers import (
    GetNetworkInteractionPathSerializer,
    GetNetworkInteractionResponseSerializer,
)

logger = logging.getLogger(__name__)


@method_decorator(name="retrieve", decorator=get_network_interaction_doc)
class GetNetworkInteractionView(PermissionRequiredMixin, viewsets.ViewSet):
    permission_required = {
        "retrieve": AccessOrchestratorPermission.NetworkAccess.get_network_interaction
    }

    def retrieve(self, request: Request, **kwargs) -> Response:
        path_serializer = GetNetworkInteractionPathSerializer(data=kwargs)
        if not path_serializer.is_valid():
            error = BaseErrorSerializer({"message": "Параметр Path невалиден."})
            return Response(error.data, status=HTTPStatus.BAD_REQUEST)

        network_interaction_id = str(
            path_serializer.validated_data["network_interaction_id"]
        )

        ...

        response_serializer = GetNetworkInteractionResponseSerializer(data=...)
        if not response_serializer.is_valid():
            error = BaseErrorSerializer(
                {
                    "message": "Ошибка сериализации ответа при получении Сетевого Взаимодействия."
                }
            )
            return Response(error.data, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return Response(response_serializer.validated_data)
