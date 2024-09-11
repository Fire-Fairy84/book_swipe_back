import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from books.models import Book
from matches.models import SwipeAction, Match
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_swipe_action_creates_match():
    client = APIClient()

    # Crear usuarios y libros
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')
    book1 = Book.objects.create(title="Book 1", author="Author 1", user=user1)
    book2 = Book.objects.create(title="Book 2", author="Author 2", user=user2)

    client.force_authenticate(user=user1)

    # user1 da like al libro de user2
    url = reverse('swipeaction-list')
    data = {'user': user1.id, 'book': book2.id, 'liked': True}  # Incluye el campo 'user'
    response = client.post(url, data, format='json')

    assert response.status_code == 201

    # user2 da like al libro de user1
    client.force_authenticate(user=user2)
    data = {'user': user2.id, 'book': book1.id, 'liked': True}  # Incluye el campo 'user'
    response = client.post(url, data, format='json')

    assert response.status_code == 201

    # Verificar si se ha creado un Match
    match_exists = Match.objects.filter(user1=user1, user2=user2).exists()
    assert match_exists
