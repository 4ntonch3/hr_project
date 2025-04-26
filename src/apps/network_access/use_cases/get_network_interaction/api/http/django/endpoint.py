import logging
from http import HTTPStatus

from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.serializers import BaseErrorSerializer
from apps.network_access.use_cases.get_network_interaction.api.http.django.openapi_doc import (
    get_network_interaction_doc,
)
from apps.network_access.use_cases.get_network_interaction.api.http.django.serializers import (
    GetNetworkInteractionPathSerializer,
    GetNetworkInteractionResponseBodySerializer,
)
from apps.network_access.use_cases.get_network_interaction.app_layer.use_case import (
    GetNetworkInteractionUseCase,
)
from apps.network_access.use_cases.get_network_interaction.domain.exceptions import (
    NetworkInteractionNotFoundError,
)
from apps.network_access.use_cases.get_network_interaction.infra.repositories.djorm.repository import (
    GetNetworkInteractionRepository,
)
from apps.users.permissions import AccessOrchestratorPermission, PermissionRequiredMixin

logger = logging.getLogger(__name__)


@method_decorator(name='retrieve', decorator=get_network_interaction_doc)
class GetNetworkInteractionView(PermissionRequiredMixin, viewsets.ViewSet):
    permission_required = {'retrieve': AccessOrchestratorPermission.NetworkAccess.get_network_interaction}

    def retrieve(self, request: Request, **kwargs) -> Response:  # noqa: U100
        path_serializer = GetNetworkInteractionPathSerializer(data=kwargs)
        if not path_serializer.is_valid():
            error = BaseErrorSerializer({'message': 'Параметр Path невалиден.'})
            return Response(error.data, status=HTTPStatus.BAD_REQUEST)

        network_interaction_id = str(path_serializer.validated_data['network_interaction_id'])

        use_case = GetNetworkInteractionUseCase(repo=GetNetworkInteractionRepository())

        try:
            ni = use_case.execute(ni_public_id=network_interaction_id)
        except NetworkInteractionNotFoundError:
            error = BaseErrorSerializer({'message': 'Сетевое Взаимодействие не найдено.'})
            return Response(error.data, status=HTTPStatus.NOT_FOUND)

        response_serializer = GetNetworkInteractionResponseBodySerializer(data=ni)
        return Response(response_serializer.validated_data)
