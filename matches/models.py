from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class SwipeAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes')  # El usuario que hace la acción
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='swipes')  # El libro sobre el que se hace la acción
    liked = models.BooleanField()  # True para like, False para dislike
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha en la que se hizo el swipe

    def __str__(self):
        return f"{self.user.username} {'liked' if self.liked else 'disliked'} {self.book.title}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='matches_as_user1')  # Primer usuario en el match
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='matches_as_user2')  # Segundo usuario en el match
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha en la que ocurrió el match

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"
