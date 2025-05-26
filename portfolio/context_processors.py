from .models import Visitante

def total_visitantes(request):
    return {
        'total_visitantes': Visitante.objects.count()
    }
