import pytest
from users.serializers import RegisterSerializer
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_serializer_creates_user():
    """
    Feature: User registration through serializer

    Scenario: A new user registers with valid data
      Given a set of valid registration data
      When the serializer validates the data
      And the user is saved
      Then the user should be created in the database
      And the user's email should be "testuser@example.com"
    """

    # Given a set of valid registration data
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    }

    # When the serializer validates the data
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()

    # And the user is saved
    user = serializer.save()

    # Then the user should be created in the database
    assert User.objects.filter(username='testuser').exists()

    # And the user's email should be "testuser@example.com"
    assert user.email == 'testuser@example.com'


@pytest.mark.django_db
def test_register_serializer_fails_with_invalid_email():
    """
    Feature: User registration through serializer

    Scenario: A user registers with an invalid email
      Given a set of registration data with an invalid email
      When the serializer validates the data
      Then the serializer should raise a validation error
    """

    # Given a set of registration data with an invalid email
    data = {
        'username': 'testuser',
        'email': 'invalid-email',
        'password': 'password123'
    }

    # When the serializer validates the data
    serializer = RegisterSerializer(data=data)

    # Then the serializer should raise a validation error
    assert not serializer.is_valid()
    assert 'email' in serializer.errors


@pytest.mark.django_db
def test_register_serializer_fails_with_duplicate_username():
    """
    Feature: User registration through serializer

    Scenario: A user registers with a duplicate username
      Given a user with the username "testuser" already exists
      When a new user registers with the same username
      Then the serializer should raise a validation error
    """

    # Given a user with the username "testuser" already exists
    User.objects.create_user(username='testuser', email='existing@example.com', password='password123')

    # When a new user registers with the same username
    data = {
        'username': 'testuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    }
    serializer = RegisterSerializer(data=data)

    # Then the serializer should raise a validation error
    assert not serializer.is_valid()
    assert 'username' in serializer.errors



