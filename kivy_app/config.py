import os

# Set the environment to 'development' or 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


if ENVIRONMENT == 'production':
    BASE_URL = 'https://8709-217-254-6-124.ngrok-free.app/api'
else:
    BASE_URL = 'http://127.0.0.1:8000/api'

ENDPOINTS = {
    'login': f'{BASE_URL}/login/',
    'registration': f'{BASE_URL}/registration/',
    'verify_token': f'{BASE_URL}/login/verify/',
    'refresh_token': f'{BASE_URL}/login/refresh/',
    'accounts': f'{BASE_URL}/accounts/',
    'account_summary': f'{BASE_URL}/account/{{account_id}}/summary/',
    'categories': f'{BASE_URL}/categories/',
    'transactions': f'{BASE_URL}/transactions/',
    # Add other endpoints as needed
}
