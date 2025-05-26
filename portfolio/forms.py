from django import forms
from .models import Projeto, Tecnologia, Experiencia
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from artigos.models import Artigo, Comentario, Avaliacao

# -- Link Magico --
class MagicLinkEmailForm(forms.Form):
    email = forms.EmailField()


# -- Formulário para registo de utilizadori
class RegistoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }


# -- Formulário para criação de projetos e tecnologias
class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = [
            'titulo',
            'descricao',
            'link_github',
            'link_demo',
            'conceitos_aplicados',
            'desafios_interessantes',
            'disciplina',
            'tecnologias_utilizadas',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'conceitos_aplicados': forms.Textarea(attrs={'rows': 3}),
            'desafios_interessantes': forms.Textarea(attrs={'rows': 3}),
            'tecnologias_utilizadas': forms.CheckboxSelectMultiple()
        }

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = '__all__'



# -- Formulário de Artigos --
class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do artigo',
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conteúdo do artigo',
                'rows': 10,
            }),
        }


# --- Formulario de Comentarios / Avaliacoes ---
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 3})
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['valor']
        widgets = {
            'valor': forms.Select(choices=[('', '---------')] + [(i, f'{i} ⭐') for i in range(1, 6)])
        }


