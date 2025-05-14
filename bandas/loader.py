from bandas.models import Banda, Album, Musica
import json
import datetime

Banda.objects.all().delete()
Album.objects.all().delete()
Musica.objects.all().delete()

# Carregar bandas
with open('json/bandas.json') as f:
    bandas = json.load(f)

    for banda_info in bandas:  # Agora iteras diretamente sobre a lista
        Banda.objects.create(
            nome=banda_info['nome'],
            genero=banda_info['genero'],
            ano_formacao=banda_info['ano_formacao'],
            biografia=banda_info['biografia'],
            foto=banda_info['foto']
        )

# Carregar álbuns e músicas
with open('json/albuns.json') as f:
    albuns = json.load(f)

    for album_info in albuns:
        banda_nome = album_info['banda']
        try:
            banda = Banda.objects.get(nome=banda_nome)
        except Banda.DoesNotExist:
            print(f"Banda '{banda_nome}' não encontrada.")
            continue

        album = Album.objects.create(
            titulo=album_info['titulo'],
            ano_lancamento=album_info['ano_lancamento'],
            banda=banda
        )

        for musica_info in album_info['musicas']:
            dur_parts = musica_info['duracao'].split(":")
            duracao = datetime.timedelta(
                hours=int(dur_parts[0]),
                minutes=int(dur_parts[1]),
                seconds=int(dur_parts[2])
            )

            Musica.objects.create(
                titulo=musica_info['titulo'],
                duracao=duracao,
                album=album,
                letra=musica_info['letra']
            )
