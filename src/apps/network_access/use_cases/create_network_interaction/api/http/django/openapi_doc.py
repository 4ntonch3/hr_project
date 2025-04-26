from http import HTTPStatus

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.core.serializers import BaseErrorSerializer
from apps.network_access.use_cases.create_network_interaction.api.http.django.serializers import (
    CreateNetworkInteractionRequestBodySerializer,
    CreateNetworkInteractionResponseBodySerializer,
)

create_network_interaction_doc = swagger_auto_schema(
    operation_description='Создать Сетевое Взаимодействие',
    operation_id='create_network_interaction',
    tags=['network_interaction'],
    request_body=CreateNetworkInteractionRequestBodySerializer,
    responses={
        HTTPStatus.OK: openapi.Response(description=None, schema=CreateNetworkInteractionResponseBodySerializer()),
        HTTPStatus.BAD_REQUEST: openapi.Response(description=None, schema=BaseErrorSerializer()),
        HTTPStatus.FORBIDDEN: openapi.Response(description=None, schema=BaseErrorSerializer()),
        HTTPStatus.INTERNAL_SERVER_ERROR: openapi.Response(description=None, schema=BaseErrorSerializer()),
    },
)
