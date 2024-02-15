from typing import Optional

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import empty

from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer para objetos Receita
    """
    chef = serializers.ReadOnlyField(source='chef.username')

    class Meta:
        model = Recipe
        fields = '__all__'
        # Informações extras para a documentação da API.
        extra_kwargs = {
            'prep_time': {'help_text': 'Tempo de preparo da receita, formato: HH:MM:SS'},
            'cook_time': {'help_text': 'Tempo de cozimento da receita, formato: HH:MM:SS'},
            'servings': {'min_value': 1},
        }

    def __init__(
            self,
            instance: Optional[Recipe] = None,
            data: Optional[dict] = empty,
            chef: Optional[User] = None,
            **kwargs
    ) -> None:
        """
        Inicialize o serializer.
        :param instance: Instância do objeto a ser serializado ou atualizado.
        :param data: Dados para serializar ou atualizar.
        :param chef: chef que está criando ou atualizando a receita.
        :param kwargs: Argumentos adicionais.
        :return: Sem retorno.
        """
        super(RecipeSerializer, self).__init__(instance=instance, data=data, **kwargs)
        # Se chef não for passado como argumento, tente obtê-lo na solicitação.
        # O chef criador da receita é necessário para criar uma nova receita. Se não for passado, tente obtê-lo na
        # solicitação, pois apenas chefs podem criar receitas.

        if not chef:
            # Tente obter o chef da solicitação.
            request = self.context.get('request')
            try:
                chef = request.user if request else None
            except:
                # Se não for possível obter o usuário da solicitação, defina chef como None.
                chef = None
        elif not chef and instance:
            # Em caso de atualização, tente obter o chef da instância já salvo.
            chef = instance.chef
        self.chef = chef

    def validate(self, attrs):
        # Verifique se o chef está definido
        if not self.chef and not attrs.get('chef'):
            # Se o chef não estiver definido, levante um erro de validação.
            raise serializers.ValidationError('Somente chefs podem cadastrar receitas.')
        elif self.chef and not attrs.get('chef'):
            # Se o chef estiver definido, mas não for passado na solicitação, defina o chef como o chef atual.
            attrs['chef'] = self.chef
        return attrs

    @property
    def validated_data(self) -> dict:
        """
        Dados validados para o serializer.
        :return: Dados validados.
        """
        # Obter os dados validados do serializer.
        data = super(RecipeSerializer, self).validated_data
        # Adicionar o chef aos dados validados.
        if self.chef:
            data['chef'] = self.chef
        return data
