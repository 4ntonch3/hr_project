from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.network_access.urls')),
    path('swagger/', include('access_orchestrator.swagger_urls')),
]
