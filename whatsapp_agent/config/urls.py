"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import Http404, HttpResponse
from django.urls import path, include
from django.views.static import serve as static_serve


def site_vitrine_home(request):
    """Sert site_vitrine/index.html tel quel à la racine du domaine."""
    index_path = settings.SITE_VITRINE_DIR / "index.html"
    if not index_path.exists():
        raise Http404
    return HttpResponse(index_path.read_text(encoding="utf-8"))


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),

    path('api/ai/', include('ai_engine.urls')),

    path('dashboard/', include('dashboard.urls')),

    # whatsapp webhook
    path('whatsapp/', include('whatsapp.urls')),

    # site vitrine (page d'accueil publique, pas de connexion requise)
    path('', site_vitrine_home, name='site_vitrine_home'),
    path(
        'assets/<path:path>',
        static_serve,
        {'document_root': settings.SITE_VITRINE_DIR / 'assets'},
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)