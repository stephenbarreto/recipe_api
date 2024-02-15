from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para objetos de usuário.
    """
    token = serializers.SerializerMethodField(
        label='Token de autenticação',
        help_text='Token de autenticação do usuário para poder usar a API',
        read_only=True,
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'token']
        labels = {
            # Nomes dos campos em português.
            'username': 'Nome de usuário',
            'password': 'Senha',
        }
        # Campos de senha não devem ser lidos, apenas escritos.
        extra_kwargs = {'password': {'write_only': True}}

    @extend_schema_field(serializers.CharField)
    def get_token(self, obj):
        """
        Obter o token de autenticação do usuário.
        """
        return Token.objects.get(user=obj).key

    def create(self, validated_data):
        """
        Método para criar um novo usuário.
        """
        # Instanciar um novo usuário com o nome de usuário e senha fornecidos.
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        # Criar um token de autenticação para o novo usuário, para poder usar a API.
        Token.objects.create(user=user)
        return user
