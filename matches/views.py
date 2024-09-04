from rest_framework import viewsets
from .models import SwipeAction, Match
from .serializers import SwipeActionSerializer, MatchSerializer
from rest_framework.permissions import IsAuthenticated


class SwipeActionViewSet(viewsets.ModelViewSet):
    queryset = SwipeAction.objects.all()
    serializer_class = SwipeActionSerializer
    permission_classes = [IsAuthenticated]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
