from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.network_access.use_cases.create_network_interaction.api.http.django.endpoint import (
    CreateNetworkInteractionView,
)
from apps.network_access.use_cases.get_network_interaction.api.http.django.endpoint import GetNetworkInteractionView

router = DefaultRouter()

api = [
    path(
        'network_interactions/<uuid:network_interaction_id>/',
        GetNetworkInteractionView.as_view({'get': 'retrieve'}),
        name='get_network_interaction',
    ),
    path(
        'network_interactions/',
        CreateNetworkInteractionView.as_view({'post': 'create'}),
        name='create_network_interaction',
    ),
]

api.extend(router.urls)

urlpatterns = [path('v1/network_access/', include(api))]
