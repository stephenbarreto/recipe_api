from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # Gerenciamento de usuários do Django Rest Framework
    path('api-auth/', include('rest_framework.urls')),
    # Documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Documentação da API com Swagger
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Adicionar as URLs dos aplicativos
    path('', include('recipe.urls')),  # Aplicativo de receitas.
    path('', include('core.urls')),  # Aplicativo com as configurações principais para uso de outros aplicativos.
]
