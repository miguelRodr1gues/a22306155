from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from .models import Tecnologia, Projeto
from .forms import ProjetoForm, TecnologiaForm

# --- Variável da senha ---
PASSWORD = "progweb2025#"

# --- Autenticação personalizada ---
def autenticacao(request):
    if request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == PASSWORD:
            request.session['autenticado'] = True
            return redirect(request.session.get('next', 'portfolio:projetos'))
        else:
            messages.error(request, "Senha incorreta.")

    request.session['next'] = request.GET.get('next', 'portfolio:projetos')
    return render(request, 'portfolio/autenticacao.html')


def sair_autenticacao(request):
    request.session['autenticado'] = False
    return redirect('portfolio:projetos')


# --- Páginas principais ---
def index_view(request):
    data_atual = datetime.now().strftime("%d/%m/%Y")
    return render(request, "portfolio/index.html", {"data": data_atual})


def sobre_view(request):
    return render(request, "portfolio/sobre.html")


def interesses_view(request):
    return render(request, "portfolio/interesses.html")


def curriculo_view(request):
    return render(request, "portfolio/cv.html")


def projetos_view(request):
    projetos = Projeto.objects.all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, "portfolio/tecnologias.html", {"tecnologias": tecnologias})


# --- CRUD de Projeto ---
def criar_projeto(request):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio:projetos')
    else:
        form = ProjetoForm()

    return render(request, 'portfolio/formulario_projeto.html', {'form': form})


def editar_projeto(request, pk):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            return redirect('portfolio:projetos')
    else:
        form = ProjetoForm(instance=projeto)

    return render(request, 'portfolio/formulario_projeto.html', {'form': form})


def apagar_projeto(request, pk):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos')

    return render(request, 'portfolio/confirmar_apagar_projeto.html', {'projeto': projeto})


# --- CRUD de Tecnologia ---
def criar_tecnologia(request):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('portfolio:tecnologias')
    else:
        form = TecnologiaForm()

    return render(request, 'portfolio/formulario_tecnologia.html', {'form': form})


def editar_tecnologia(request, pk):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    tecnologia = get_object_or_404(Tecnologia, pk=pk)
    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES, instance=tecnologia)
        if form.is_valid():
            form.save()
            return redirect('portfolio:tecnologias')
    else:
        form = TecnologiaForm(instance=tecnologia)

    return render(request, 'portfolio/formulario_tecnologia.html', {'form': form})


def apagar_tecnologia(request, pk):
    if not request.session.get('autenticado'):
        return redirect(f"{reverse('portfolio:autenticacao')}?next={request.path}")

    tecnologia = get_object_or_404(Tecnologia, pk=pk)
    if request.method == 'POST':
        tecnologia.delete()
        return redirect('portfolio:tecnologias')

    return render(request, 'portfolio/confirmar_apagar_tecnologia.html', {'tecnologia': tecnologia})
