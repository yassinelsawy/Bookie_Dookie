from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from Books.models import Book
from Books.serializers import AddBookSerializer, GetBookSerializer


# Create your views here.
class AddBook(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddBookSerializer(data=request.data)
        if serializer.is_valid():
            # Save the book using the serializer
            serializer.save()
            return Response({"message": "Book added successfully"}, status=201)
        return Response(serializer.errors, status=400)


class GetBook(APIView):
    def get(self, request, *args, **kwargs):
        book_id = request.query_params.get('id')  # Get the book ID from query parameters
        if book_id:
            book = get_object_or_404(Book, id=book_id)  # Retrieve the book by ID
            serializer = GetBookSerializer(book)
            return Response(serializer.data, status=200)
        else:
            books = Book.objects.all()  # Retrieve all books if no ID is provided
            serializer = GetBookSerializer(books, many=True)
            return Response(serializer.data, status=200)