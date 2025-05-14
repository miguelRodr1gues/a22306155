from django.contrib import admin
from .models import Banda, Album, Musica

@admin.register(Banda)
class BandaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'ano_formacao')
    search_fields = ('nome', 'genero')

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ano_lancamento', 'banda')
    search_fields = ('titulo', 'banda__nome')
    list_filter = ('ano_lancamento', 'banda')

@admin.register(Musica)
class MusicaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'album', 'duracao')
    search_fields = ('titulo', 'album__titulo')
    list_filter = ('album',)
