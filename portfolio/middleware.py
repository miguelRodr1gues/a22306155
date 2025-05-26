from .models import Visitante
from django.utils.deprecation import MiddlewareMixin

class ContadorVisitantesMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        ip = self.get_client_ip(request)
        if not Visitante.objects.filter(ip_address=ip).exists():
            Visitante.objects.create(ip_address=ip)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
