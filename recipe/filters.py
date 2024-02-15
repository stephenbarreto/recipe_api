import django_filters

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """
    Filtrar por objetos Receita, com base no nome e no nome do chef.
    """
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='Nome da Receita',
        help_text='Nome da receita',
    )
    chef_username = django_filters.CharFilter(
        field_name='chef__username', lookup_expr='iexact', label='Nome de usuário do Chef',
        help_text='Nome de usuário do chef da receita',
    )

    class Meta:
        model = Recipe
        fields = ['name', 'chef_username']
