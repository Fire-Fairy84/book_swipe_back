from rest_framework import serializers
from .models import SwipeAction, Match


class SwipeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwipeAction
        fields = ['id', 'user', 'book', 'liked', 'created_at']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'created_at']
