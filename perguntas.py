from bandas.models import Banda, Album, Musica
from datetime import timedelta

# Exibir todas as bandas ordenadas pelo nome
bandas = Banda.objects.order_by('nome')
for banda in bandas:
    print(banda.nome)

print("\n--- Fim da lista de bandas ---\n")

# Exibir os álbuns da banda "Silk Sonic"
nome_banda = "Silk Sonic"
albuns = Album.objects.filter(banda__nome=nome_banda).order_by('ano_lancamento')
for album in albuns:
    print(album.titulo)

print("\n--- Fim dos álbuns da banda Silk Sonic ---\n")

# Exibir álbuns lançados entre 2000 e 2010
ano_inicio = 2000
ano_fim = 2010
albuns = Album.objects.filter(ano_lancamento__range=(ano_inicio, ano_fim)).order_by('ano_lancamento')
for album in albuns:
    print(album.titulo, album.ano_lancamento)

print("\n--- Fim dos álbuns de 2000 a 2010 ---\n")

# Exibir playlist de músicas do álbum "FanMail"
titulo_album = "FanMail"
musicas = Musica.objects.filter(album__titulo=titulo_album)
playlist = [musica.link for musica in musicas]
print(playlist)

print("\n--- Fim da playlist de FanMail ---\n")

# Exibir álbuns com músicas maiores que 3 minutos
albuns = Album.objects.all()
for album in albuns:
    num_musicas_longas = album.musicas.filter(duracao__gt=timedelta(minutes=3)).count()
    if num_musicas_longas > 0:
        print(album.titulo, num_musicas_longas)

print("\n--- Fim dos álbuns com músicas longas ---\n")

# Exibir músicas com a palavra "take" no título
palavra = "take"
musicas = Musica.objects.filter(titulo__icontains=palavra)
for musica in musicas:
    print(musica.titulo)

print("\n--- Fim das músicas com a palavra 'take' ---\n")

# Exibir músicas da banda "Maroon 5"
musicas = Musica.objects.filter(album__banda__nome="Maroon 5")
for musica in musicas:
    print(musica.titulo)

print("\n--- Fim das músicas da banda Maroon 5 ---\n")

# Exibir o número de músicas por álbum
albuns = Album.objects.all()
for album in albuns:
    num_musicas = album.musicas.count()
    print(album.titulo, num_musicas)

print("\n--- Fim da contagem de músicas por álbum ---\n")

# Exibir a duração total das músicas do álbum "TLC"
musicas = Musica.objects.filter(album__titulo="7/27")
duracao_total = sum(musica.duracao.total_seconds() for musica in musicas)
print(f"Duração total: {duracao_total} segundos")

print("\n--- Fim da duração total do álbum TLC ---\n")

# Exibir bandas com mais de 1 álbum
bandas = Banda.objects.all()
for banda in bandas:
    num_albuns = Album.objects.filter(banda=banda).count()
    if num_albuns > 1:
        print(banda.nome, num_albuns)

print("\n--- Fim das bandas com mais de 1 álbum ---\n")
