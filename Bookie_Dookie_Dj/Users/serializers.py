from rest_framework import serializers
from .models import User, UserBorrowedBook


class signUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_staff']

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff')
        user = User.objects.create_user(**validated_data)
        user.is_staff = is_staff
        user.save()
        return user

class UserBorrow(serializers.ModelSerializer):
    class Meta:
        model = UserBorrowedBook
        fields = ['book', 'borrow_date',]

