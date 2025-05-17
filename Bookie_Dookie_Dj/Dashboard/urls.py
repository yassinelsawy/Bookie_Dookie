

from django.urls import path
from . import views
from Dashboard.views import UsersList

urlpatterns = [
    path('get_users/', UsersList.as_view(), name='dashboard'),
]