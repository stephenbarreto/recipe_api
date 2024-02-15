from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# Cria um roteador e registra a view de receitas.
router = DefaultRouter()
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    # Inclui as URLs do roteador.
    path('', include(router.urls)),
]
