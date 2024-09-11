import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from books.models import Book
from matches.models import Match
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_swipe_action_creates_match():
    """
    Feature: Swipe action and match creation

    Scenario: Two users like each other's books and create a match
      Given a user "user1" with password "12345" exists
      And a user "user2" with password "12345" exists
      And user1 owns a book titled "Book 1"
      And user2 owns a book titled "Book 2"
      When user1 likes "Book 2"
      And user2 likes "Book 1"
      Then a match should be created between "user1" and "user2"
    """

    # Given a user "user1" and a user "user2" exist
    client = APIClient()
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')

    # And user1 owns a book titled "Book 1"
    book1 = Book.objects.create(title="Book 1", author="Author 1", user=user1)

    # And user2 owns a book titled "Book 2"
    book2 = Book.objects.create(title="Book 2", author="Author 2", user=user2)

    # When user1 likes "Book 2"
    client.force_authenticate(user=user1)
    swipe_url = reverse('swipeaction-list')
    swipe_data_1 = {'user': user1.id, 'book': book2.id, 'liked': True}
    response_1 = client.post(swipe_url, swipe_data_1, format='json')

    # Assert the response status is 201
    assert response_1.status_code == 201, f"Error in user1's like action: {response_1.content}"

    # And user2 likes "Book 1"
    client.force_authenticate(user=user2)
    swipe_data_2 = {'user': user2.id, 'book': book1.id, 'liked': True}
    response_2 = client.post(swipe_url, swipe_data_2, format='json')

    # Assert the response status is 201
    assert response_2.status_code == 201, f"Error in user2's like action: {response_2.content}"

    # Then a match should be created between "user1" and "user2"
    match_exists = Match.objects.filter(
        user1__in=[user1, user2], user2__in=[user1, user2]
    ).exists()
    assert match_exists, "No match was created"


@pytest.mark.django_db
def test_swipe_action_fails_with_invalid_data():
    """
    Feature: Swipe action and match creation

    Scenario: A user attempts to like a book with invalid data
      Given a user "user1" with password "12345" exists
      And a book exists owned by "user2"
      When user1 likes the book with invalid data
      Then the swipe action should fail with a validation error
    """

    # Given a user "user1" and "user2" exist
    client = APIClient()
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')

    # And a book exists owned by user2
    book2 = Book.objects.create(title="Book 2", author="Author 2", user=user2)

    # When user1 likes the book with invalid data (missing book ID)
    client.force_authenticate(user=user1)
    invalid_swipe_data = {'user': user1.id, 'liked': True}
    response = client.post(reverse('swipeaction-list'), invalid_swipe_data, format='json')

    # Then the swipe action should fail
    assert response.status_code == 400, "Swipe action should have failed due to missing book ID"


@pytest.mark.django_db
def test_no_match_created_with_one_like():
    """
    Feature: Swipe action and match creation

    Scenario: Only one user likes a book, no match is created
      Given a user "user1" with password "12345" exists
      And a user "user2" with password "12345" exists
      And user1 owns a book titled "Book 1"
      And user2 owns a book titled "Book 2"
      When user1 likes "Book 2"
      Then no match should be created
    """

    # Given a user "user1" and "user2" exist
    client = APIClient()
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')

    # And user1 owns a book
    book1 = Book.objects.create(title="Book 1", author="Author 1", user=user1)

    # And user2 owns a book
    book2 = Book.objects.create(title="Book 2", author="Author 2", user=user2)

    # When user1 likes "Book 2"
    client.force_authenticate(user=user1)
    swipe_data = {'user': user1.id, 'book': book2.id, 'liked': True}
    response = client.post(reverse('swipeaction-list'), swipe_data, format='json')

    # Assert the response status is 201
    assert response.status_code == 201, "Error in user1's like action"

    # Then no match should be created yet
    match_exists = Match.objects.filter(
        user1__in=[user1, user2], user2__in=[user1, user2]
    ).exists()
    assert not match_exists, "Match should not be created with only one like"



@pytest.mark.django_db
def test_unauthenticated_user_cannot_like():
    """
    Feature: Swipe action and match creation

    Scenario: An unauthenticated user tries to like a book
      Given a book exists owned by "user2"
      When an unauthenticated user tries to like the book
      Then the swipe action should fail with a 403 error
    """

    # Given a user "user2" and a book exist
    user2 = User.objects.create_user(username='user2', password='12345')
    book2 = Book.objects.create(title="Book 2", author="Author 2", user=user2)

    # When an unauthenticated user tries to like the book
    client = APIClient()
    swipe_data = {'user': None, 'book': book2.id, 'liked': True}  # Unauthenticated
    response = client.post(reverse('swipeaction-list'), swipe_data, format='json')

    # Then the swipe action should fail with a 403 error
    assert response.status_code == 401, "Unauthenticated user should not be able to like a book"
