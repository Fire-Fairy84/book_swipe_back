from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'user', 'user_name']
        read_only_fields = ['user']

