from rest_framework import viewsets
from .models import SwipeAction, Match
from .serializers import SwipeActionSerializer, MatchSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class SwipeActionViewSet(viewsets.ModelViewSet):
    queryset = SwipeAction.objects.all()
    serializer_class = SwipeActionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Crear un SwipeAction
        response = super().create(request, *args, **kwargs)

        # Comprobar si se debe crear un Match
        user = request.user
        book_id = request.data.get('book')
        liked = request.data.get('liked', False)

        if liked:
            # Obtener el libro que fue likeado
            try:
                book_owner = SwipeAction.objects.get(book_id=book_id).book.user

                # Verificar si el propietario del libro ha dado like a un libro del usuario actual
                if SwipeAction.objects.filter(user=book_owner, book__user=user, liked=True).exists():
                    # Crear un Match si ambos han dado like
                    Match.objects.create(user1=user, user2=book_owner)
                    return Response({"detail": "Match created!"}, status=status.HTTP_201_CREATED)

            except SwipeAction.DoesNotExist:
                return response

        return response


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
