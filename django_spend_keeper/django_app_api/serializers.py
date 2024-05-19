from rest_framework import serializers
from .models import User, Account, Transaction, Category, Saving


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["name", "total_balance"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "type", "description"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["amount", "account", "category", "note", "datetime"]

    def update(self, instance, validated_data):
        new_amount = validated_data.get('amount', instance.amount)
        if abs(instance.amount) == abs(new_amount):
            raise serializers.ValidationError("The new amount is the same as the old amount.")
        return super().update(instance, validated_data)


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'
