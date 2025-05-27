import pytest
from django.urls import reverse, resolve
from django.test import Client
from bandas.models import Banda, Album, Musica
from artigos.models import Artigo, Comentario, Avaliacao
from portfolio.models import Disciplina, Projeto, Tecnologia


@pytest.mark.django_db
class ModelsTest:
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
        nomes = [t.nome for t in projeto.tecnologias_utilizadas.all()]
        assert "React" in nomes
        assert "Next.js" in nomes

    def test_projeto_disciplina(self):
        projeto = Projeto.objects.get(pk=3)
        assert projeto.disciplina.nome == "Fundamentos de Programação"


@pytest.mark.django_db
class UrlsTest:
    fixtures = ['db.json']

    def test_reverse_and_resolve_artigo_detalhe(self):
        url = reverse('artigo_detalhe', args=[5])
        assert url == "/artigos/5/"
        resolver = resolve("/artigos/5/")
        assert resolver.view_name == "artigo_detalhe"

    def test_reverse_and_resolve_lista_bandas(self):
        url = reverse('lista_bandas')
        assert url == "/bandas/"
        resolver = resolve("/bandas/")
        assert resolver.view_name == "lista_bandas"

    def test_reverse_and_resolve_tecnologias(self):
        url = reverse('lista_tecnologias')
        assert url == "/tecnologias/"
        resolver = resolve("/tecnologias/")
        assert resolver.view_name == "lista_tecnologias"

    def test_reverse_and_resolve_detalhe_banda(self):
        url = reverse('detalhe_banda', args=[1])
        assert url == "/bandas/1/"
        resolver = resolve("/bandas/1/")
        assert resolver.view_name == "detalhe_banda"

    def test_reverse_and_resolve_lista_projetos(self):
        url = reverse('lista_projetos')
        assert url == "/portfolio/projetos/"
        resolver = resolve("/portfolio/projetos/")
        assert resolver.view_name == "lista_projetos"

    def test_reverse_and_resolve_detalhe_projeto(self):
        url = reverse('detalhe_projeto', args=[1])
        assert url == "/portfolio/projetos/1/"
        resolver = resolve("/portfolio/projetos/1/")
        assert resolver.view_name == "detalhe_projeto"


@pytest.mark.django_db
class ViewsTest:
    fixtures = ['db.json']

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = Client()

    def test_artigo_detalhe_view(self):
        response = self.client.get(reverse('artigo_detalhe', args=[5]))
        assert response.status_code == 200
        assert "NEGAO" in response.content.decode()
        assert "artigos/artigo_detalhe.html" in [t.name for t in response.templates]

    def test_lista_artigos_view(self):
        response = self.client.get(reverse('lista_artigos'))
        assert response.status_code == 200
        assert "NEGAO" in response.content.decode()
        assert "artigos/lista_artigos.html" in [t.name for t in response.templates]

    def test_lista_bandas_view(self):
        response = self.client.get(reverse('lista_bandas'))
        assert response.status_code == 200
        assert "Destiny's Child" in response.content.decode()
        assert "bandas/lista_bandas.html" in [t.name for t in response.templates]

    def test_detalhe_banda_view(self):
        response = self.client.get(reverse('detalhe_banda', args=[1]))
        assert response.status_code == 200
        assert "Say My Name" in response.content.decode()
        assert "bandas/detalhe_banda.html" in [t.name for t in response.templates]

    def test_lista_tecnologias_view(self):
        response = self.client.get(reverse('lista_tecnologias'))
        assert response.status_code == 200
        assert "Next.js" in response.content.decode()
        assert "portfolio/lista_tecnologias.html" in [t.name for t in response.templates]

    def test_lista_projetos_view(self):
        response = self.client.get(reverse('lista_projetos'))
        assert response.status_code == 200
        assert "Humans VS Zombies" in response.content.decode()
        assert "portfolio/lista_projetos.html" in [t.name for t in response.templates]

    def test_detalhe_projeto_view(self):
        response = self.client.get(reverse('detalhe_projeto', args=[1]))
        assert response.status_code == 200
        html = response.content.decode()
        assert "Humans VS Zombies" in html
        assert "Herança" in html
        assert "portfolio/detalhe_projeto.html" in [t.name for t in response.templates]
