import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from books.models import Book
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_book_view():
    """
    Feature: Book creation through API

    Scenario: A user creates a new book with valid data
      Given a user "testuser" with password "12345" exists
      And the user is authenticated
      When the user sends a POST request to create a book with title "Cien Años de Soledad"
      Then the response status code should be 201
      And the created book should have the title "Cien Años de Soledad"
    """

    # Given a user "testuser" exists
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')

    # And the user is authenticated
    client.force_authenticate(user=user)

    # When the user sends a POST request to create a book
    url = reverse('book-list')
    data = {
        'title': 'Cien Años de Soledad',
        'author': 'Gabriel García Márquez',
        'description': 'A novel about a family',
    }
    response = client.post(url, data, format='json')

    # Then the response status code should be 201
    assert response.status_code == 201

    # And the created book should have the title "Cien Años de Soledad"
    assert response.data['title'] == 'Cien Años de Soledad'


@pytest.mark.django_db
def test_my_books_view():
    """
    Feature: Fetch user-specific books

    Scenario: A user fetches their own books
      Given a user "testuser" with password "12345" exists
      And the user is authenticated
      And the user owns two books titled "Book 1" and "Book 2"
      When the user sends a GET request to fetch their books
      Then the response status code should be 200
      And the user should receive a list of 2 books
    """

    # Given a user "testuser" exists
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')

    # And the user is authenticated
    client.force_authenticate(user=user)

    # And the user owns two books titled "Book 1" and "Book 2"
    Book.objects.create(title="Book 1", author="Author 1", description="Desc 1", user=user)
    Book.objects.create(title="Book 2", author="Author 2", description="Desc 2", user=user)

    # When the user sends a GET request to fetch their books
    url = reverse('my-books')
    response = client.get(url)

    # Then the response status code should be 200
    assert response.status_code == 200

    # And the user should receive a list of 2 books
    assert len(response.data) == 2


@pytest.mark.django_db
def test_create_book_fails_with_missing_fields():
    """
    Feature: Book creation through API

    Scenario: A user attempts to create a new book with missing fields
      Given a user "testuser" with password "12345" exists
      And the user is authenticated
      When the user sends a POST request to create a book without a title
      Then the response status code should be 400
      And the response should contain an error message for the title field
    """

    # Given a user "testuser" exists
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')

    # And the user is authenticated
    client.force_authenticate(user=user)

    # When the user sends a POST request to create a book without a title
    url = reverse('book-list')
    data = {
        'author': 'Gabriel García Márquez',
        'description': 'A novel about a family',
        # Missing title
    }
    response = client.post(url, data, format='json')

    # Then the response status code should be 400
    assert response.status_code == 400

    # And the response should contain an error message for the title field
    assert 'title' in response.data


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_book():
    """
    Feature: Book creation through API

    Scenario: An unauthenticated user attempts to create a new book
      When the unauthenticated user sends a POST request to create a book
      Then the response status code should be 401
      And the book should not be created
    """

    # Given an unauthenticated user
    client = APIClient()

    # When the unauthenticated user sends a POST request to create a book
    url = reverse('book-list')
    data = {
        'title': 'Cien Años de Soledad',
        'author': 'Gabriel García Márquez',
        'description': 'A novel about a family',
    }
    response = client.post(url, data, format='json')

    # Then the response status code should be 401 (Unauthorized)
    assert response.status_code == 401

    # And the book should not be created
    assert Book.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_fetch_another_users_books():
    """
    Feature: Fetch user-specific books

    Scenario: A user attempts to fetch books owned by another user
      Given a user "user1" owns two books titled "Book 1" and "Book 2"
      And a user "user2" exists
      When user2 sends a GET request to fetch their own books
      Then the response status code should be 200
      And the list of books should be empty
    """

    # Given user1 exists and owns two books
    client = APIClient()
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')

    Book.objects.create(title="Book 1", author="Author 1", description="Desc 1", user=user1)
    Book.objects.create(title="Book 2", author="Author 2", description="Desc 2", user=user1)

    # When user2 sends a GET request to fetch their books
    client.force_authenticate(user=user2)
    url = reverse('my-books')
    response = client.get(url)

    # Then the response status code should be 200
    assert response.status_code == 200

    # And the list of books should be empty (since user2 has no books)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_nonexistent_book_returns_404():
    """
    Feature: Fetch book details

    Scenario: A user attempts to fetch details for a book that doesn't exist
      Given a user "testuser" exists
      And a book with ID 9999 does not exist
      When the user sends a GET request to fetch the book details
      Then the response status code should be 404
    """

    # Given a user "testuser" exists
    client = APIClient()
    user = User.objects.create_user(username='testuser', password='12345')

    # When the user sends a GET request to fetch a book that doesn't exist
    client.force_authenticate(user=user)
    url = reverse('book-detail', kwargs={'pk': 9999})  # Non-existent book ID
    response = client.get(url)

    # Then the response status code should be 404
    assert response.status_code == 404



