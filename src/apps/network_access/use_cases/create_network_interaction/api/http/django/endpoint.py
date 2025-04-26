import json
import logging
from http import HTTPStatus

from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.serializers import BaseErrorSerializer
from apps.network_access.use_cases.create_network_interaction.api.http.django.openapi_doc import (
    create_network_interaction_doc,
)
from apps.network_access.use_cases.create_network_interaction.api.http.django.serializers import (
    CreateNetworkInteractionRequestBodySerializer,
    CreateNetworkInteractionResponseBodySerializer,
)
from apps.network_access.use_cases.create_network_interaction.app_layer.use_case import (
    CreateNetworkInteractionError,
    CreateNetworkInteractionUseCase,
)
from apps.network_access.use_cases.create_network_interaction.infra.repositories.djorm.repository import (
    CreateNetworkInteractionRepository,
)
from apps.users.permissions import AccessOrchestratorPermission, PermissionRequiredMixin

logger = logging.getLogger(__name__)


@method_decorator(name='create', decorator=create_network_interaction_doc)
class CreateNetworkInteractionView(PermissionRequiredMixin, viewsets.ViewSet):
    permission_required = {'create': AccessOrchestratorPermission.NetworkAccess.create_network_interaction}

    def create(self, request: Request, **kwargs) -> Response:
        body_serializer = CreateNetworkInteractionRequestBodySerializer(data=request.data)
        if not body_serializer.is_valid():
            error = BaseErrorSerializer({'message': 'Некорректные параметры запроса.'})
            return Response(error.data, status=HTTPStatus.BAD_REQUEST)

        use_case = CreateNetworkInteractionUseCase(repo=CreateNetworkInteractionRepository())

        try:
            ni_public_id = use_case.execute(
                arch_interaction_guid=body_serializer.validated_data['arch_interaction_guid'],
                src_arch_stand_guid=body_serializer.validated_data['src_arch_stand_guid'],
                src_arch_component_guid=body_serializer.validated_data['src_arch_component_guid'],
                dst_arch_stand_guid=body_serializer.validated_data['dst_arch_stand_guid'],
                dst_arch_component_guid=body_serializer.validated_data['dst_arch_component_guid'],
                src_network_zone_name=body_serializer.validated_data['src_network_zone_name'],
                dst_network_zone_name=body_serializer.validated_data['dst_network_zone_name'],
                protocol_to_ports=json.loads(body_serializer.validated_data['protocol_to_ports']),
                user_id=request.user.id,
            )
        except CreateNetworkInteractionError as exc:
            error = BaseErrorSerializer(
                {'message': f'Некорректные данные для создания Сетевого Взаимодействия. Детали: {exc.details}'}
            )
            return Response(error.data, status=HTTPStatus.BAD_REQUEST)

        response_serializer = CreateNetworkInteractionResponseBodySerializer(data={'id': ni_public_id})
        return Response(response_serializer.validated_data)
