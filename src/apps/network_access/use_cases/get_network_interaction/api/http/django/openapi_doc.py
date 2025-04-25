from http import HTTPStatus

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.network_access.use_cases.get_network_interaction.api.http.django.serializers import (
    GetNetworkInteractionResponseSerializer,
)
from src.apps.core.serializers import BaseErrorSerializer

get_network_interaction_doc = swagger_auto_schema(
    operation_description='Получить Сетевое Взаимодействие',
    operation_id='get_network_interaction',
    tags=['network_interaction'],
    responses={
        HTTPStatus.OK: openapi.Response(description=None, schema=GetNetworkInteractionResponseSerializer()),
        HTTPStatus.BAD_REQUEST: openapi.Response(description=None, schema=BaseErrorSerializer()),
        HTTPStatus.FORBIDDEN: openapi.Response(description=None, schema=BaseErrorSerializer()),
        HTTPStatus.NOT_FOUND: openapi.Response(description=None, schema=BaseErrorSerializer()),
        HTTPStatus.INTERNAL_SERVER_ERROR: openapi.Response(description=None, schema=BaseErrorSerializer()),
    },
)
