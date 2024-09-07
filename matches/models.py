from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class SwipeAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swipes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='swipes')
    liked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {'liked' if self.liked else 'disliked'} {self.book.title}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"
