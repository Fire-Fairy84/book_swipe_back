import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from books.models import Book
from django.contrib.auth.models import User

## Verificar la creación de un libro a través de la API con autenticación
@pytest.mark.django_db
def test_create_book_view():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_authenticate(user=user)

    url = reverse('book-list')
    data = {
        'title': 'Cien Años de Soledad',
        'author': 'Gabriel García Márquez',
        'description': 'A novel about a family',
    }
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['title'] == 'Cien Años de Soledad'

## Verificar que la view devuelve los libros del usuario autenticado
@pytest.mark.django_db
def test_my_books_view():
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_authenticate(user=user)

    Book.objects.create(title="Book 1", author="Author 1", description="Desc 1", user=user)
    Book.objects.create(title="Book 2", author="Author 2", description="Desc 2", user=user)

    url = reverse('my-books')  # Asegúrate de que este es el nombre correcto de tu ruta
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2



