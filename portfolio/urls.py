from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [

    # --- Experiencias ---
    path('experiencia/', views.experiencias, name='experiencias'),
    path('experiencia/novo/', views.criar_experiencia, name='criar_experiencia'),
    path('experiencia/<int:pk>/', views.detalhe_experiencia, name='detalhe_experiencia'),
    path('experiencia/<int:pk>/editar/', views.editar_experiencia, name='editar_experiencia'),

    # --- Páginas Públicas ---
    path('', views.index_view, name='index'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('interesses/', views.interesses_view, name='interesses'),
    path('cv/', views.curriculo_view, name='curriculo'),

    # --- Autenticação Tradicional ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    # --- Login com Link Mágico ---
    path('login/magic/', views.request_magic_link, name='request_magic_link'),
    path('login/magic/<str:token>/', views.magic_login, name='magic_login'),
    path('link-expirado/', views.link_expirado_view, name='link_expirado'),

    # --- Projetos ---
    path('projetos/', views.projetos_view, name='projetos'),
    path('projetos/criar/', views.criar_projeto, name='criar_projeto'),
    path('projetos/<int:pk>/editar/', views.editar_projeto, name='editar_projeto'),
    path('projetos/<int:pk>/apagar/', views.apagar_projeto, name='apagar_projeto'),

    # --- Tecnologias ---
    path('tecnologias/', views.tecnologias_view, name='tecnologias'),
    path('tecnologias/criar/', views.criar_tecnologia, name='criar_tecnologia'),
    path('tecnologias/<int:pk>/editar/', views.editar_tecnologia, name='editar_tecnologia'),
    path('tecnologias/<int:pk>/apagar/', views.apagar_tecnologia, name='apagar_tecnologia'),

    # --- Artigos ---
    path('artigos/', views.artigos, name='artigos'),
    path('artigos/novo/', views.criar_artigo, name='criar_artigo'),
    path('artigo/<int:pk>/', views.detalhe_artigo, name='detalhe_artigo'),
    path('artigos/<int:pk>/editar/', views.editar_artigo, name='editar_artigo'),
    path('artigos/<int:pk>/apagar/', views.apagar_artigo, name='apagar_artigo'),
]
