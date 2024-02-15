from django.urls import path

from . import views

urlpatterns = [
    # URL para cadastrar um novo chef.
    path('chefs/create/', views.ChefCreateView.as_view(), name='chef-create'),
]
