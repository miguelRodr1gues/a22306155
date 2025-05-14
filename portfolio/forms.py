from django import forms
from .models import Projeto, Tecnologia


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

