from django.urls import path
from rest_framework import views

from Books.views import AddBook, GetBook

urlpatterns = [
    path('add_book/', AddBook.as_view(), name='add_book'),
    path('get_book/', GetBook.as_view(), name='get_book'),
]