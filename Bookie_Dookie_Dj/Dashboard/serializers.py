from Users.models import User
from rest_framework import serializers


class getUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
