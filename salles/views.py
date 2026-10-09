"""Taches 3, 4, 5 (et bonus) : vues de l'API.

A FAIRE :
  - SalleViewSet (ModelViewSet), avec l'action `occupation` (tache 5)
  - ReservationViewSet (ModelViewSet), avec perform_create (tache 3)
"""
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime

from .permissions import IsOwnerOrReadOnly
from .serializers import ReservationSerializer, SalleSerializer  # noqa: F401  (a utiliser)
from .models import Reservation, Salle  # noqa: F401  (a utiliser)


class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    
    def get_permissions(self):
      if self.request.method in permissions.SAFE_METHODS:
          return [permissions.AllowAny()]
      return [permissions.IsAdminUser()]

    @action(detail=True, methods=['get'])
    def occupation(self, request, pk=None):
        salle = self.get_object() # met 404 si la salle n'existe pas
        debut = parse_datetime(request.query_params.get("debut", ""))
        fin = parse_datetime(request.query_params.get("fin", ""))
        if not debut or not fin or fin <= debut:
            return Response({"detail": "debut et fin sont nécessaires, fin > debut."}, status=400)

        reserve = 0
        for r in salle.reservations.filter(statut="CONFIRMEE", debut__lt=fin, fin__gt=debut):
            reserve += (min(r.fin, fin) - max(r.debut, debut)).total_seconds()

        return Response({"taux_occupation": reserve / (fin - debut).total_seconds()})

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)