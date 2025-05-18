from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    borrowed_books = models.ManyToManyField(
        'Books.Book',
        through='UserBorrowedBook',
        related_name='borrowers'
    )
    wishlist = models.ManyToManyField(Book, related_name='wishlisted_by', blank=True)
class UserBorrowedBook(models.Model):
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Books.Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
