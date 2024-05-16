from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, AccountSerializer
from .serializers import TransactionSerializer, CategorySerializer, SavingSerializer
from .utils import generate_jwt_token, update_account_balance
from .models import Account, Category, Transaction


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response(token)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountsListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Retrieve all Account instances associated with the authenticated user
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the authenticated user with the newly created Account instance
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Filter accounts based on the authenticated user and account ID
        return self.queryset.filter(user=self.request.user, id=self.kwargs['pk'])


class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions based on the authenticated user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the authenticated user with the new Transaction object
        serializer.save(user=self.request.user)
        update_account_balance(serializer)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions based on the authenticated user and transaction ID
        return self.queryset.filter(user=self.request.user, id=self.kwargs['pk'])

    def perform_update(self, serializer):
        # Update the account's total balance when a transaction is updated
        previous_transaction = self.get_object()
        previous_amount = previous_transaction.amount
        previous_is_income = previous_transaction.is_income
        serializer.save()
        current_transaction = serializer.instance
        if previous_is_income:
            account = current_transaction.account
            account.total_balance -= previous_amount
            account.total_balance += current_transaction.amount
            account.save()
        else:
            account = current_transaction.account
            account.total_balance += previous_amount
            account.total_balance -= current_transaction.amount
            account.save()

    def perform_destroy(self, instance):
        # Adjust the account's total balance when a transaction is deleted
        account = instance.account
        if instance.is_income:
            account.total_balance -= instance.amount
        else:
            account.total_balance += instance.amount
        account.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class SavingCreateView(generics.CreateAPIView):
    serializer_class = SavingSerializer
    permission_classes = [IsAuthenticated]
