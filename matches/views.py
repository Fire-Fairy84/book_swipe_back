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

        response = super().create(request, *args, **kwargs)

        user = request.user
        book_id = request.data.get('book')
        liked = request.data.get('liked', False)

        if liked:
            try:
                book_owner = SwipeAction.objects.get(book_id=book_id).book.user

                if SwipeAction.objects.filter(user=book_owner, book__user=user, liked=True).exists():
                    Match.objects.create(user1=user, user2=book_owner)
                    return Response({"detail": "Match created!"}, status=status.HTTP_201_CREATED)

            except SwipeAction.DoesNotExist:
                return response

        return response


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsAuthenticated]
