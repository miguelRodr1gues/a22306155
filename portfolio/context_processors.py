from django.core.cache import cache
from .models import Visitante

def total_visitantes(request):
    total = cache.get('total_visitantes')
    if total is None:
        total = Visitante.objects.count()
        cache.set('total_visitantes', total)
    return {'total_visitantes': total}
