from django.contrib.auth import get_user_model
from django.test import TestCase
from decimal import Decimal
from django_app_api.models import Account, Category, Transaction, Saving

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpass123')

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpass123')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.account = Account.objects.create(user=self.user, name='Main Account', total_balance=Decimal('100.00'))

    def test_account_creation(self):
        self.assertEqual(self.account.name, 'Main Account')
        self.assertEqual(self.account.total_balance, Decimal('100.00'))


class CategoryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpass')

    def tearDown(self):
        Category.objects.all().delete()
        User.objects.all().delete()

    def test_category_creation(self):
        # Ensure no conflicting categories exist
        Category.objects.filter(user=self.user, name='Groceries', type=Category.EXPENSE).delete()

        category = Category.objects.create(user=self.user, name='Groceries', type=Category.EXPENSE)
        self.assertEqual(category.name, 'Groceries')
        self.assertEqual(category.type, Category.EXPENSE)


class TransactionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpass')

        # Ensure no conflicting categories exist
        Category.objects.filter(user=self.user, name='Salary', type=Category.INCOME).delete()
        self.account = Account.objects.create(user=self.user, name='Main Account', total_balance=Decimal('100.00'))
        self.category = Category.objects.create(user=self.user, name='Salary', type=Category.INCOME)

    def tearDown(self):
        Transaction.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            amount=1000,
            note='Monthly salary'
        )
        self.assertEqual(transaction.amount, 1000)


class SavingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.account = Account.objects.create(user=self.user, name='Savings Account', total_balance=Decimal('500.00'))

    def test_saving_creation(self):
        saving = Saving.objects.create(user=self.user, amount=Decimal('150.00'), account=self.account)
        self.assertEqual(saving.amount, Decimal('150.00'))
        self.assertEqual(saving.account, self.account)
