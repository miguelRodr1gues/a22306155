from django.urls import path
from . import views  # importamos views para poder usar as suas funções

app_name = 'portfolio'

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('interesses/', views.interesses_view, name='interesses'),
    path("cv/", views.curriculo_view, name="curriculo"),
    
    # Projetos
    path('projetos/', views.projetos_view, name='projetos'),
    path('projetos/criar/', views.criar_projeto, name='criar_projeto'),
    path('projetos/<int:pk>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projetos/<int:pk>/apagar/', views.apagar_projeto, name='apagar_projeto'),
    
    # Tecnologias
    path("tecnologias/", views.tecnologias_view, name="tecnologias"),
    path('tecnologias/criar/', views.criar_tecnologia, name='criar_tecnologia'),
    path('tecnologias/<int:pk>/editar/', views.editar_tecnologia, name='editar_tecnologia'),
    path('tecnologias/<int:pk>/apagar/', views.apagar_tecnologia, name='apagar_tecnologia'),

    # Autenticação
    path('autenticacao/', views.autenticacao, name='autenticacao'),
    path('sair/', views.sair_autenticacao, name='sair_autenticacao'),
]
