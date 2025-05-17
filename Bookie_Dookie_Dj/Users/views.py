from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from Users.serializers import signUpSerializer
from Users.models import User



# Create your views here.
class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        serializer = signUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User Registered Successfully", status=201)
        return Response(serializer.errors, status=400)
class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # user = User.objects.filter(username=username, password=password).first()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "is_staff": user.is_staff}, status=201)
        else:
            return Response({"error": "Invalid credentials"}, status=401)
