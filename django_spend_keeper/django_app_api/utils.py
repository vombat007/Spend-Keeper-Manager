from rest_framework_simplejwt.tokens import RefreshToken


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

    return token


def update_account_balance(serializer):
    transaction = serializer.instance
    account = transaction.account
    if transaction.is_income:
        account.total_balance += transaction.amount
    else:
        account.total_balance -= transaction.amount
    account.save()
