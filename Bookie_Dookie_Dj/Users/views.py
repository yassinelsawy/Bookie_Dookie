from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Books.models import Book
from Books.serializers import GetBookSerializer
from Users.serializers import signUpSerializer, UserBorrow
from Users.models import User, UserBorrowedBook


# Create your views here.
class SignUp(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = signUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User Registered Successfully", status=201)
        return Response(serializer.errors, status=400)
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        # user = User.objects.filter(username=username, password=password).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "is_staff": user.is_staff}, status=201)
        else:
            return Response({"error": "Invalid credentials"}, status=401)

class GetUserRole(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:

            return Response({"is_staff": user.is_staff}, status=200)
        else:
            return Response({"error": "User not authenticated"}, status=401)

class LogOut(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=200)



# Borrow Requests
class GetBorrowings(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        borrowed_books = UserBorrowedBook.objects.filter(user=user)
        data = [
            {
                "book": GetBookSerializer(borrowing.book).data,  # Serialize the whole book data
                "borrow_date": borrowing.borrow_date
            }
            for borrowing in borrowed_books
        ]
        return Response(data, status=200)
class ReturnBook(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user
        book_id = request.query_params.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        if book in user.borrowed_books.all():
            book.book_state = 1
            book.save()
            UserBorrowedBook.objects.filter(user=user, book=book).delete()
            return Response({"message": "Book returned successfully"}, status=200)
        else:
            return Response({"message": "Book returned successfully"}, status=200)
class BorrowBook(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.query_params.get('book_id')
        book = Book.objects.get(id=book_id)
        if book.book_state == 1:
            book.book_state = 0
            book.save()
            UserBorrowedBook.objects.create(user=user, book=book)
            return Response({"message": "Book borrowed successfully"}, status=201)
        else:
            return Response({"error": "Book is not available"}, status=400)
# Wishlist
class Wishlist(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            # Handle anonymous user
            return Response([], status=200)
        user = request.user
        wishlist = user.wishlist.all()
        serializer = GetBookSerializer(wishlist, many=True)
        return Response(serializer.data, status=200)
class AddToWishlist(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        book_id = request.query_params.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        user.wishlist.add(book)
        return Response({"message": "Book added to wishlist"}, status=201)
class RemoveFromWishlist(APIView):
    def delete(self, request, *args, **kwargs):
        user = request.user
        book_id = request.query_params.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        user.wishlist.remove(book)
        return Response({"message": "Book removed from wishlist"}, status=200)

