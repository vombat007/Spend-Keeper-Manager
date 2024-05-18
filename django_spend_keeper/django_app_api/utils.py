from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, User


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return token


def create_default_categories(user):
    default_categories = [
        {'name': 'Salary', 'type': Category.INCOME, 'description': 'Income from salary.'},
        {'name': 'Gifts', 'type': Category.INCOME, 'description': 'Income from gifts.'},
        {'name': 'Other', 'type': Category.INCOME, 'description': 'Income from other.'},

        {'name': 'Groceries', 'type': Category.EXPENSE, 'description': 'Expenses on groceries.'},
        {'name': 'Haus', 'type': Category.EXPENSE, 'description': 'Expenses on haus.'},
        {'name': 'Restaurant', 'type': Category.EXPENSE, 'description': 'Expenses on restaurant.'},
        {'name': 'Gifts', 'type': Category.EXPENSE, 'description': 'Expenses on gifts.'},
        {'name': 'Shopping', 'type': Category.EXPENSE, 'description': 'Expenses on shopping.'},
        {'name': 'Health', 'type': Category.EXPENSE, 'description': 'Expenses on health.'},
        {'name': 'Transport', 'type': Category.EXPENSE, 'description': 'Expenses on transport.'},
        {'name': 'Leisure', 'type': Category.EXPENSE, 'description': 'Expenses on leisure.'},
        {'name': 'Family', 'type': Category.EXPENSE, 'description': 'Expenses on family.'},
    ]

    for category_data in default_categories:
        Category.objects.create(user=user, **category_data)
