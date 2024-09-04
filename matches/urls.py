from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SwipeActionViewSet, MatchViewSet

router = DefaultRouter()
router.register(r'swipes', SwipeActionViewSet)
router.register(r'matches', MatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
