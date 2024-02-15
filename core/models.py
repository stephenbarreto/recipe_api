from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Modelo base para todos os modelos do projeto. Classe abstrata que adiciona campos de data de criação e atualização
    usados em todos os modelos do projeto.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
