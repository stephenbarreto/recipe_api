from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .filters import RecipeFilter
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Este conjunto de visualizações fornece automaticamente ações "list", "create", "retrieve", "update" e "destroy"
    para receitas.
    """
    # Modelo de dados que será usado
    model = Recipe
    # Consulta que será usada para obter os objetos
    queryset = Recipe.objects.all()
    # Serializador que será usado para serializar e desserializar os objetos
    serializer_class = RecipeSerializer
    # Permissões que serão usadas para verificar se o usuário pode executar a ação. Neste caso, qualquer usuário
    # autenticado pode criar, atualizar e excluir receitas, mas qualquer pessoa pode listar e ver os detalhes das
    # receitas.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Filtros que serão usados para filtrar os objetos. Neste caso, usaremos o DjangoFilterBackend para permitir que
    # os usuários filtrem receitas por nome e nome do chef.
    filter_backends = [DjangoFilterBackend]
    # Classe de filtro que será usada para filtrar os objetos.
    filterset_class = RecipeFilter

    def get_serializer(self, *args, **kwargs):
        """
        Obtenha o serializador para a solicitação.
        """
        # Adicionar o usuário autenticado como o chef da receita, para que o usuário não precise passar o chef na
        # solicitação.
        kwargs['chef'] = self.request.user
        return super(RecipeViewSet, self).get_serializer(*args, **kwargs)
