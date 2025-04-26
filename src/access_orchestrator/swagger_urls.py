from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.network_access.urls import api as network_access_api

schema_network_access_view = get_schema_view(
    openapi.Info(title='Access Orchestrator API', default_version='v1'),
    generator_class=OpenAPISchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[path('v1/network_access/', include(network_access_api))],
)

urlpatterns_matching = {'network_access': schema_network_access_view}


def get_path_name_by_schema(schema_key: str) -> str:
    return f'schema-{schema_key}-swagger-ui'


urlpatterns = [
    path(f'{key}/', schema_view.with_ui('swagger'), name=get_path_name_by_schema(key))
    for key, schema_view in urlpatterns_matching.items()
]
