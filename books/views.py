from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class MyBooksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_books = Book.objects.filter(user=request.user)
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data)