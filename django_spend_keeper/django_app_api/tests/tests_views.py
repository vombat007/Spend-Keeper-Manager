from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_app_api.models import Account, Category, Transaction
import uuid

User = get_user_model()


class RegisterViewTest(APITestCase):
    def test_user_registration(self):
        url = reverse('registration')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class AccountsListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_accounts(self):
        url = reverse('user-account-detail')
        Account.objects.create(user=self.user, name='Main Account', total_balance='100.00')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_account(self):
        url = reverse('user-account-detail')
        data = {
            'name': 'Savings Account',
            'total_balance': '200.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'Savings Account')


class TransactionListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuseremail@com', password='testpass')
        self.client.login(email='testuseremail@com', password='testpass')

        self.account = Account.objects.create(user=self.user, name='Main Account', total_balance='100.00')
        self.category_name = 'Salary-' + str(uuid.uuid4())
        self.category = Category.objects.create(user=self.user, name=self.category_name, type=Category.INCOME)
        self.client.force_authenticate(user=self.user)

    def test_create_transaction(self):
        url = reverse('transaction-create')
        data = {
            'amount': '50.00',
            'account': self.account.id,
            'category': self.category.id,
            'note': 'Test transaction'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().amount, 50.00)


class CategoryListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuseremail@com', password='testpass')
        self.client.login(email='testuseremail@com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'New Category-' + str(uuid.uuid4()),
            'type': Category.EXPENSE,
            'description': 'Test category'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
