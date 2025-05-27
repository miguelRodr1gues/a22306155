import pytest
from django.urls import reverse, resolve
from django.test import Client
from bandas.models import Banda, Album, Musica
from artigos.models import Artigo, Autor, Comentario, Avaliacao
from portfolio.models import Disciplina, Tecnologia, Projeto

@pytest.mark.django_db
class TestModels:
    fixtures = ['db.json']

    def test_banda_str(self):
        banda = Banda.objects.get(pk=1)
        assert str(banda) == "Destiny's Child"

    def test_album_str(self):
        album = Album.objects.get(pk=1)
        assert str(album) == "Survivor"

    def test_album_banda_relation(self):
        album = Album.objects.get(pk=1)
        assert album.banda.nome == "Destiny's Child"

    def test_musica_album_relation(self):
        musica = Musica.objects.get(pk=1)
        assert musica.album.titulo == "Survivor"

    def test_artigo_str(self):
        artigo = Artigo.objects.get(pk=5)
        assert artigo.titulo == "NEGAO"

    def test_avaliacao_valor(self):
        avaliacao = Avaliacao.objects.get(pk=2)
        assert 0 <= avaliacao.valor <= 5

    def test_comentario_artigo_relation(self):
        comentario = Comentario.objects.get(pk=2)
        assert comentario.artigo.pk == 5

    def test_tecnologia_str(self):
        tecnologia = Tecnologia.objects.get(nome="Next.js")
        assert "React" in tecnologia.descricao

    def test_disciplina_str(self):
        disciplina = Disciplina.objects.get(pk=4)
        assert str(disciplina).startswith("Programação Web")

    def test_projeto_str(self):
        projeto = Projeto.objects.get(pk=1)
        assert str(projeto) == "Humans VS Zombies"

    def test_projeto_tecnologias(self):
        projeto = Projeto.objects.get(pk=2)
        tecnologias = [t.nome for t in projeto.tecnologias_utilizadas.all()]
        assert "React" in tecnologias
        assert "Next.js" in tecnologias

    def test_projeto_disciplina(self):
        projeto = Projeto.objects.get(pk=3)
        assert projeto.disciplina.nome == "Fundamentos de Programação"


@pytest.mark.django_db
class TestUrls:
    fixtures = ['db.json']

    def test_reverse_artigo_detalhe(self):
        url = reverse('artigo_detalhe', args=[5])
        assert url == "/artigos/5/"

    def test_resolve_artigo_detalhe(self):
        resolver = resolve("/artigos/5/")
        assert resolver.view_name == "artigo_detalhe"

    def test_reverse_lista_bandas(self):
        url = reverse('lista_bandas')
        assert url == "/bandas/"

    def test_reverse_lista_tecnologias(self):
        url = reverse('lista_tecnologias')
        assert url == "/tecnologias/"

    def test_reverse_detalhe_banda(self):
        url = reverse('detalhe_banda', args=[1])
        assert url == "/bandas/1/"

    def test_reverse_lista_projetos(self):
        url = reverse('lista_projetos')
        assert url == "/portfolio/projetos/"

    def test_reverse_detalhe_projeto(self):
        url = reverse('detalhe_projeto', args=[1])
        assert url == "/portfolio/projetos/1/"

    def test_resolve_lista_projetos(self):
        resolver = resolve('/portfolio/projetos/')
        assert resolver.view_name == "lista_projetos"

    def test_resolve_detalhe_projeto(self):
        resolver = resolve('/portfolio/projetos/1/')
        assert resolver.view_name == "detalhe_projeto"


@pytest.mark.django_db
class TestViews:
    fixtures = ['db.json']

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()

    def test_artigo_detalhe_view(self):
        response = self.client.get(reverse('artigo_detalhe', args=[5]))
        assert response.status_code == 200
        content = response.content.decode()
        assert "NEGAO" in content
        assert "Bernardo Jerónimo" in content
        assert "artigos/artigo_detalhe.html" in [t.name for t in response.templates]

    def test_lista_bandas_view(self):
        response = self.client.get(reverse('lista_bandas'))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Destiny's Child" in content
        assert "bandas/lista_bandas.html" in [t.name for t in response.templates]

    def test_detalhe_banda_view(self):
        response = self.client.get(reverse('detalhe_banda', args=[1]))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Say My Name" in content  # música de Destiny's Child
        assert "bandas/detalhe_banda.html" in [t.name for t in response.templates]

    def test_lista_tecnologias_view(self):
        response = self.client.get(reverse('lista_tecnologias'))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Next.js" in content
        assert "portfolio/lista_tecnologias.html" in [t.name for t in response.templates]

    def test_lista_artigos_view(self):
        response = self.client.get(reverse('lista_artigos'))
        assert response.status_code == 200
        content = response.content.decode()
        assert "NEGAO" in content
        assert "artigos/lista_artigos.html" in [t.name for t in response.templates]

    def test_lista_projetos_view(self):
        response = self.client.get(reverse('lista_projetos'))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Humans VS Zombies" in content
        assert "portfolio/lista_projetos.html" in [t.name for t in response.templates]

    def test_detalhe_projeto_view(self):
        response = self.client.get(reverse('detalhe_projeto', args=[1]))
        assert response.status_code == 200
        content = response.content.decode()
        assert "Humans VS Zombies" in content
        assert "Herança" in content
        assert "portfolio/detalhe_projeto.html" in [t.name for t in response.templates]
