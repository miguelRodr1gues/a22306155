from django.http import HttpResponse
import datetime

def index_view(request):
    return HttpResponse("Olá noob, esta é a pagina web mais básica do mundo!")

def hora_atual_view(request):
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    return HttpResponse(f"A hora atual é {agora}")

def mensagem_motivacional_view(request):
    return HttpResponse("Você é capaz de tudo! Nunca subestime o poder de um café e uma boa linha de código ☕💻")

def lista_favoritos_view(request):
    linguagens = ["Java", "JavaScript", "Python", "Kotlin"]
    lista_formatada = "<ul>" + "".join(f"<li>{linguagem}</li>" for linguagem in linguagens) + "</ul>"
    return HttpResponse(f"<h2>Linguagens Favoritas:</h2>{lista_formatada}")
