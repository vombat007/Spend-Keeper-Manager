from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from .models import User, UserAccount, Transaction, Category, Saving


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['name', 'total_balance']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'
