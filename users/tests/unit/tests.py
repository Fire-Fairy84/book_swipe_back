import pytest
from users.serializers import RegisterSerializer
from django.contrib.auth.models import User


## Verificar que el serializador crea un usuario correctamente
@pytest.mark.django_db
def test_register_serializer_creates_user():
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()

    assert User.objects.filter(username='testuser').exists()
    assert user.email == 'testuser@example.com'
