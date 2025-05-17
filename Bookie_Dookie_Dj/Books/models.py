from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    cover_url = models.CharField(max_length=200)
    description = models.TextField()
    book_state = models.BooleanField(default=True)

