
from django.urls import path
from . import views
from Users.views import SignUp, Login, Wishlist, AddToWishlist, \
    RemoveFromWishlist, GetBorrowings, BorrowBook, ReturnBook

urlpatterns = [
path('login/', Login.as_view(), name='login'),
path('signup/', SignUp.as_view(), name='signup'),

path('get_borrow/', GetBorrowings.as_view(), name='get_borrow'),
path('borrow/', BorrowBook.as_view(), name='borrow'),
path('return/', ReturnBook.as_view(), name='return'),

path('get_wishlist/', Wishlist.as_view(), name='get_wishlist'),
path('wishlist/', AddToWishlist.as_view(), name='wishlist'),
path('remove_wishlist/', RemoveFromWishlist.as_view(), name='remove_wishlist'),

]