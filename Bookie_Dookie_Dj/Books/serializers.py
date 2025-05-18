from rest_framework import serializers
from Books.models import Book

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'cover_url', 'description']

class GetBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'cover_url', 'description', 'book_state']
