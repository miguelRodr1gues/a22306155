# noobsite/urls.py

from django.urls import path
from . import views  # importamos views para poder usar as suas funções

urlpatterns = [
    path('index/', views.index_view),
    path('hora/', views.hora_atual_view),
    path('motivacao/', views.mensagem_motivacional_view),
    path('favoritos/', views.lista_favoritos_view),
]
