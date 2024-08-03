import os

# Set the environment to 'development' or 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

if ENVIRONMENT == 'development':
    BASE_URL = 'https://087c-2003-c1-b709-2b00-9019-5e30-46d0-f283.ngrok-free.app/api'
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
    'logout': f'{BASE_URL}/logout/',
    # Add other endpoints as needed
}
