from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="autor", null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="artigos")
    criado_em = models.DateTimeField(auto_now_add=True)

    def media_avaliacoes(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return sum(avaliacao.valor for avaliacao in avaliacoes) / avaliacoes.count()
        return None

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="comentarios")
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário por {self.autor.nome} em {self.artigo.titulo}"

class Avaliacao(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name="avaliacoes")
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="avaliacoes")
    valor = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.autor.nome} - {self.valor}⭐ para {self.artigo.titulo}"
