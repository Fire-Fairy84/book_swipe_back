import pytest
from matches.models import Match
from django.contrib.auth.models import User


## Verificar que se crea un Match correctamente
@pytest.mark.django_db
def test_create_match():
    user1 = User.objects.create_user(username='user1', password='12345')
    user2 = User.objects.create_user(username='user2', password='12345')

    match = Match.objects.create(user1=user1, user2=user2)

    assert str(match) == f"Match between {user1.username} and {user2.username}"
