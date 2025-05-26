from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('noobsite/', include('noobsite.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('accounts/', include('allauth.urls')),
]
