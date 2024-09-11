from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='books')

    def __str__(self):
        return self.title
