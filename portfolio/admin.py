from django.contrib import admin
from .models import Disciplina, Tecnologia, Projeto, ImagemProjeto, Visitante, Experiencia


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'docentes')
    search_fields = ('nome', 'docentes')
    list_filter = ('ano', 'semestre')


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'listar_projetos_associados')
    search_fields = ('nome',)

    def listar_projetos_associados(self, obj):
        return ", ".join(obj.nomes_projetos_associados())
    listar_projetos_associados.short_description = 'Projetos Associados'


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'disciplina')
    search_fields = ('titulo', 'descricao')
    list_filter = ('disciplina', 'tecnologias_utilizadas')


@admin.register(ImagemProjeto)
class ImagemProjetoAdmin(admin.ModelAdmin):
    list_display = ('projeto', 'descricao')
    search_fields = ('descricao', 'projeto__titulo')


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'data')
    search_fields = ('ip_address',)
    ordering = ('-data',)


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cargo', 'descricao')
    search_fields = ('empresa', 'cargo')
    list_filter = ('dataInicio', 'dataFim')


