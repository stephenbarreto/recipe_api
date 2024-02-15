from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer


class ChefCreateView(generics.CreateAPIView):
    """
    View para criar um novo chef.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Permitir que qualquer pessoa crie um novo chef.
    permission_classes = []

    def perform_create(self, serializer):
        """
        Método para criar um novo chef.
        """
        user = serializer.save()

        response_data = {
            'user_id': user.id,
            'username': user.username,
            # Token de autenticação do usuário para poder usar a API
            'token': Token.objects.get(user=user).key
        }
        return Response(response_data)
