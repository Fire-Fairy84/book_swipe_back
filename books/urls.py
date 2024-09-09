from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, MyBooksView

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('mybooks/', MyBooksView.as_view(), name='my-books'),
    path('', include(router.urls)),
]
