from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import BaseModel


class Recipe(BaseModel):
    """
    Objeto de receita
    """
    name = models.CharField(max_length=255, verbose_name='Nome', help_text='Nome da receita.')
    description = models.TextField(
        verbose_name='Descrição', help_text='Descrição da receita.', blank=True, null=True
    )
    ingredients = models.TextField(verbose_name='Ingredientes', help_text='Ingredientes da receita.')
    instructions = models.TextField(verbose_name='Instruções', help_text='Instruções da receita.')
    prep_time = models.DurationField(
        verbose_name='Prep Time', help_text='Tempo de preparo da receita.',
        validators=[
            # Validação para garantir que o tempo de preparo seja igual ou superior a 1 minuto.
            MinValueValidator(
                limit_value=timezone.timedelta(minutes=1),
                message='O tempo de preparo deve ser igual ou superior a 1 minuto.'
            ),
        ]
    )
    cook_time = models.DurationField(
        verbose_name='Tempo de cozimento', help_text='Tempo de cozimento da receita.',
        validators=[
            # Validação para garantir que o tempo de cozimento seja igual ou superior a 0 minutos.
            MinValueValidator(
                limit_value=timezone.timedelta(minutes=0),
                message='O tempo de cozimento deve ser igual ou superior a 0 minutos.',
            )
        ]
    )
    servings = models.IntegerField(
        verbose_name='Porções', help_text='Porções da receita.', default=1,
        validators=[MinValueValidator(limit_value=1, message='As porções devem ser iguais ou superiores a 1.')]
    )
    chef = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='chef', help_text='Chef que criou a receita.',
        related_name='recipes',
    )

    def __str__(self):
        return self.name

    def validate(self):
        """
        Método para validar o objeto de receita antes de salvar.
        """
        if self.chef is None:
            # Se a receita não estiver associada a um chef, levantar um ValueError.
            raise ValueError('A receita deve estar associada a um chef.')
