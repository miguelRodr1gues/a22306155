from django.db import models

class Banda(models.Model):
    nome = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    ano_formacao = models.IntegerField()
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='bandas_fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.ano_formacao})"

class Album(models.Model):
    titulo = models.CharField(max_length=100)
    ano_lancamento = models.IntegerField()
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name='albuns')
    capa = models.ImageField(upload_to='albuns_capas/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano_lancamento}) - {self.banda.nome}"

class Musica(models.Model):
    titulo = models.CharField(max_length=100)
    duracao = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='musicas')
    letra = models.TextField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.album.titulo}"
