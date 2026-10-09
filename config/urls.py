"""Routes racine du projet."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Connexion/deconnexion pour la Browsable API de DRF
    path("api-auth/", include("rest_framework.urls")),
    # Routes de l'API (a completer dans salles/urls.py)
    path("api/", include("salles.urls")),
    path('', RedirectView.as_view(url='api/', permanent=False)),
]
