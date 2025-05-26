from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta


# -- Modelo para criação de projetos e tecnologias
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField(choices=[(1, '1º Ano'), (2, '2º Ano'), (3, '3º Ano')])
    semestre = models.IntegerField(choices=[(1, '1º Semestre'), (2, '2º Semestre')])
    docentes = models.CharField(max_length=255)
    link_moodle = models.URLField(blank=True, null=True)
    link_ulusofona = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.ano}º ano - {self.semestre}º semestre)"


class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    logotipo = models.ImageField(upload_to='logos_tecnologias/')
    link = models.URLField(blank=True, null=True)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    def nomes_projetos_associados(self):
        return [projeto.titulo for projeto in self.projetos_associados.all()]


class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link_github = models.URLField(blank=True, null=True)
    link_demo = models.URLField(blank=True, null=True)
    conceitos_aplicados = models.TextField()
    desafios_interessantes = models.TextField()
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='projetos')
    tecnologias_utilizadas = models.ManyToManyField(Tecnologia, related_name='projetos_associados')

    def __str__(self):
        return self.titulo


class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='imagens_projetos/')
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Imagem do projeto: {self.projeto.titulo}"


class Visitante(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address


# --- Model Experiencia ---
class Experiencia(models.Model):

    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    descricao = models.TextField()
    dataInicio = models.DateTimeField(auto_now_add=True)
    dataFim = models.DateTimeField(auto_now_add=True)
    projetos = models.ManyToManyField(Projeto, blank=True, related_name='experiencias')
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='experiencias')


# -- Token Temporário para Link Mágico

class MagicLinkToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)  # marca se o token já foi usado

    @property
    def expira_em(self):
        return self.created_at + timedelta(minutes=15)

    def is_valid(self):
        return not self.used and timezone.now() < self.expira_em

    def __str__(self):
        return f"Token para {self.user.email} (usado: {self.used})"
