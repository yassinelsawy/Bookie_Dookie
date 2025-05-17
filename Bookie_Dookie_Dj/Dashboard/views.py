from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# from django.contrib.auth.models import User  # Use the default Django User model

from Users.models import User
from Dashboard.serializers import getUsers


# Create your views here.
class UsersList(APIView):
    def get(self, request, *args, **kwargs):

        users = list(User.objects.all())
        print(users)
        serializer = getUsers(users, many=True)
        return Response(serializer.data, status=200)
