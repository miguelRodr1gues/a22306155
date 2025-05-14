from .models import Visitante
from django.core.cache import cache

class ContadorVisitantesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip and not Visitante.objects.filter(ip_address=ip).exists():
            Visitante.objects.create(ip_address=ip)
            cache.set('total_visitantes', Visitante.objects.count())
        return self.get_response(request)
