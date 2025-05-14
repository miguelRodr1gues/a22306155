from django.contrib import admin
from .models import Autor, Artigo, Comentario, Avaliacao

class AutorAdmin(admin.ModelAdmin):
    list_display = ("nome", "email")
    search_fields = ("nome", "email")

class ArtigoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "criado_em")
    list_filter = ("autor", "criado_em")
    search_fields = ("titulo", "conteudo")

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("autor", "artigo", "criado_em")
    list_filter = ("artigo", "autor", "criado_em")
    search_fields = ("conteudo",)

class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("autor", "artigo", "valor")
    list_filter = ("valor", "artigo", "autor")

admin.site.register(Autor, AutorAdmin)
admin.site.register(Artigo, ArtigoAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)