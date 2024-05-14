from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, AccountSerializer
from .serializers import TransactionSerializer, CategorySerializer, SavingSerializer
from .utils import generate_jwt_token
from .models import Account, Category


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt_token(user)
            return Response(token)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Retrieve the UserAccount associated with the authenticated user
        user_account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(user_account)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # Set the user to the authenticated user
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user_account = Account.objects.get(user=request.user)
        serializer = AccountSerializer(user_account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_account = Account.objects.get(user=request.user)
        user_account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class SavingCreateView(generics.CreateAPIView):
    serializer_class = SavingSerializer
    permission_classes = [IsAuthenticated]
