from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

# --- Autenticação / Login ---
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# --- Models e Forms ---
from .models import Projeto, Tecnologia, MagicLinkToken, Experiencia
from .forms import ProjetoForm, TecnologiaForm, RegistoForm, MagicLinkEmailForm, ArtigoForm, ComentarioForm, AvaliacaoForm, ExperienciaForm

# --- Email ---
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

# --- Models Artigos ---
from artigos.models import Artigo, Autor, Comentario, Avaliacao


# --- Verificação de Superuser ---
def is_superuser(user):
    return user.is_authenticated and user.is_superuser


# --- Pagina de Testes ---
def pagina_testes(request):
    return render(request, 'portfolio/testes.html')


# --- Pagina de Experiencia ---
def experiencias(request):
    lista_experiencias = Experiencia.objects.order_by('dataInicio')
    return render(request, 'portfolio/experiencias.html', {'experiencias': lista_experiencias})


# --- Detalhes da Experiencia ---
@login_required(login_url='portfolio:login')
def detalhe_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    cargo = experiencia.cargo.all()


    return render(request, 'portfolio/detalhe_experiencia.html', {
        'experiencia': experiencia,
        'cargo': cargo,
    })


# --- Pagina de Criacao de Experiencias ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def criar_experiencia(request):
    form = ExperienciaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portfolio:experiencias')
    return render(request, 'portfolio/formulario_experiencia.html', {'form': form})


# --- Pagina de Edicao de Projetos ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def editar_experiencia(request, pk):
    experiencia = get_object_or_404(Experiencia, pk=pk)
    form = ExperienciaForm(request.POST or None, instance=experiencia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:experiencias')
    return render(request, 'portfolio/formulario_experiencia.html', {
        'form': form,
        'experiencia': experiencia
    })



# --- Pagina de Artigos ---
def artigos(request):
    lista_artigos = Artigo.objects.select_related('autor').order_by('-criado_em')
    return render(request, 'portfolio/artigos.html', {'artigos': lista_artigos})


# --- Pagina com detalhes do artigo - Comentarios/Avalicoes ---
@login_required(login_url='portfolio:login')
def detalhe_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    comentarios = artigo.comentarios.select_related('autor').order_by('-criado_em')

    autor, _ = Autor.objects.get_or_create(
        user=request.user,
        defaults={
            "nome": request.user.get_full_name() or request.user.username,
            "email": request.user.email
        }
    )

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        avaliacao_form = AvaliacaoForm(request.POST)

        conteudo_valido = comentario_form.is_valid() and comentario_form.cleaned_data.get("conteudo")
        avaliacao_valida = avaliacao_form.is_valid() and avaliacao_form.cleaned_data.get("valor")

        if not conteudo_valido and not avaliacao_valida:
            comentario_form.add_error(None, "Tens de escrever um comentário, dar uma avaliação ou ambos.")
        else:
            if conteudo_valido:
                Comentario.objects.create(
                    artigo=artigo,
                    autor=autor,
                    conteudo=comentario_form.cleaned_data['conteudo']
                )

            if avaliacao_valida:
                Avaliacao.objects.update_or_create(
                    artigo=artigo,
                    autor=autor,
                    defaults={'valor': avaliacao_form.cleaned_data['valor']}
                )

            return redirect('portfolio:detalhe_artigo', pk=pk)

    else:
        comentario_form = ComentarioForm()
        avaliacao_form = AvaliacaoForm()

    media = artigo.media_avaliacoes()

    return render(request, 'portfolio/detalhe_artigo.html', {
        'artigo': artigo,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'avaliacao_form': avaliacao_form,
        'media_avaliacoes': media,
    })



# --- Pagina de Criacao de Artigos ---
@login_required(login_url='portfolio:login')
def criar_artigo(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST)
        if form.is_valid():
            artigo = form.save(commit=False)
            autor, _ = Autor.objects.get_or_create(
                user=request.user,
                defaults={
                    "nome": request.user.get_full_name() or request.user.username,
                    "email": request.user.email
                }
            )
            artigo.autor = autor
            artigo.save()
            return redirect('portfolio:artigos')
    else:
        form = ArtigoForm()
    return render(request, 'portfolio/formulario_artigo.html', {'form': form})


# --- Pagina de Edicao de Artigos (apenas o user que publicou pode editar) ---
@login_required(login_url='portfolio:login')
def editar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    autor, _ = Autor.objects.get_or_create(
        user=request.user,
        defaults={
            "nome": request.user.get_full_name() or request.user.username,
            "email": request.user.email
        }
    )
    if artigo.autor != autor:
        return HttpResponseForbidden("Não tens permissão para editar este artigo.")

    if request.method == 'POST':
        form = ArtigoForm(request.POST, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('portfolio:artigos')
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'portfolio/formulario_artigo.html', {'form': form, 'artigo': artigo})


# --- Pagina de Remover Artigos (apenas o user que publicou pode apagar) ---
@login_required(login_url='portfolio:login')
def apagar_artigo(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    autor, _ = Autor.objects.get_or_create(
        user=request.user,
        defaults={
            "nome": request.user.get_full_name() or request.user.username,
            "email": request.user.email
        }
    )
    if artigo.autor != autor:
        return HttpResponseForbidden("Não tens permissão para apagar este artigo.")

    if request.method == 'POST':
        artigo.delete()
        return redirect('portfolio:artigos')
    return render(request, 'portfolio/confirmar_apagar_artigo.html', {'artigo': artigo})


# --- Link Mágico ---
def request_magic_link(request):
    if request.method == 'POST':
        form = MagicLinkEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = MagicLinkToken.objects.create(user=user)

                link = request.build_absolute_uri(
                    reverse('portfolio:magic_login', args=[str(token.token)])
                )

                send_mail(
                    'O teu link mágico de login',
                    f'Clica aqui para entrares: {link}',
                    'noreply@teusite.com',
                    [email],
                    fail_silently=False,
                )

                # Aqui: renderiza a página de sucesso (link enviado)
                return render(request, 'portfolio/link_sent.html')

            except User.DoesNotExist:
                form.add_error('email', 'Este e-mail não está registado.')
    else:
        form = MagicLinkEmailForm()

    return render(request, 'portfolio/request_link.html', {'form': form})


# --- Se o token tiver expirado manda para a pagina de link expirado ---
def magic_login(request, token):
    try:
        token_obj = MagicLinkToken.objects.get(token=token)

        if token_obj.used:
            return render(request, 'portfolio/link_expirado.html', {'mensagem': 'Este link já foi usado.'})

        if timezone.now() > token_obj.expira_em:
            return render(request, 'portfolio/link_expirado.html', {'mensagem': 'Este link expirou.'})

        user = token_obj.user

        # Define o backend explicitamente, necessário quando há múltiplos backends
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        token_obj.used = True
        token_obj.save()

        return redirect('portfolio:index')

    except MagicLinkToken.DoesNotExist:
        return render(request, 'portfolio/link_expirado.html', {'mensagem': 'Link inválido.'})


# --- Renderiza quando o link magico expira ---
def link_expirado_view(request):
    return render(request, 'portfolio/link_expirado.html')


# --- Páginas Públicas ---
def index_view(request):
    return render(request, 'portfolio/index.html')

def sobre_view(request):
    return render(request, 'portfolio/sobre.html')

def interesses_view(request):
    return render(request, 'portfolio/interesses.html')

def curriculo_view(request):
    return render(request, 'portfolio/cv.html')



# --- Reset de Password ---
def reset_password_view(request):
    mensagem = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        nova_password = request.POST.get('password')
        confirmar_password = request.POST.get('confirm_password')

        try:
            user = User.objects.get(username=username)

            if nova_password != confirmar_password:
                mensagem = "As palavras-passe não coincidem."
            elif len(nova_password) < 6:
                mensagem = "A nova palavra-passe deve ter pelo menos 6 caracteres."
            else:
                user.password = make_password(nova_password)
                user.save()
                mensagem = "Palavra-passe alterada com sucesso."
        except User.DoesNotExist:
            mensagem = "Utilizador não encontrado."

    return render(request, 'portfolio/reset_password.html', {'mensagem': mensagem})


# --- Login ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or 'portfolio:index'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            error = "Credenciais inválidas."
            return render(request, 'portfolio/login.html', {
                'error': error,
                'next': request.POST.get('next', '')
            })
    else:
        return render(request, 'portfolio/login.html', {
            'next': request.GET.get('next', '')

        })



# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('portfolio:index')



# --- Registo ---
def register_view(request):
    form = RegistoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('portfolio:index')

    return render(request, 'portfolio/register.html', {'form': form})



# --- Listagens (Utilizadores autenticados) - Paginas Projetos e Tecnologias ---
def projetos_view(request):
    projetos = Projeto.objects.all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})


def tecnologias_view(request):
    tecnologias = Tecnologia.objects.all()
    return render(request, 'portfolio/tecnologias.html', {'tecnologias': tecnologias})



# --- CRUD de Projetos (Apenas Superuser) ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def criar_projeto(request):
    form = ProjetoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/formulario_projeto.html', {'form': form})


# --- Pagina de Edicao de Projetos ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def editar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    form = ProjetoForm(request.POST or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/formulario_projeto.html', {
        'form': form,
        'projeto': projeto
    })


# --- Pagina de Remover Tecnologias ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def apagar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos')
    return render(request, 'portfolio/confirmar_apagar_projeto.html', {'projeto': projeto})



# --- CRUD de Tecnologias (Apenas Superuser) ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def criar_tecnologia(request):
    form = TecnologiaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/formulario_tecnologia.html', {'form': form})


# --- Pagina de Edicao de Tecnologias ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def editar_tecnologia(request, pk):
    tecnologia = get_object_or_404(Tecnologia, pk=pk)
    form = TecnologiaForm(request.POST or None, instance=tecnologia)
    if form.is_valid():
        form.save()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/formulario_tecnologia.html', {
        'form': form,
        'tecnologia': tecnologia
    })


# --- Pagina de Remover Tecnologias ---
@user_passes_test(is_superuser, login_url='portfolio:login')
def apagar_tecnologia(request, pk):
    tecnologia = get_object_or_404(Tecnologia, pk=pk)
    if request.method == 'POST':
        tecnologia.delete()
        return redirect('portfolio:tecnologias')
    return render(request, 'portfolio/confirmar_apagar_tecnologia.html', {'tecnologia': tecnologia})