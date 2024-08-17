import os
import cloudinary

# Set the environment to 'development' or 'production'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    BASE_URL = 'https://8ee2-2003-c1-b723-4e00-6c91-fe00-45ad-c85a.ngrok-free.app/api'
    WINDOWS_SIZE = (0, 0)
else:
    BASE_URL = 'http://127.0.0.1:8000/api'
    WINDOWS_SIZE = (412, 915)  # Example size, change as needed

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

    # Url for cloudinary cloud folder
    'icon_url': 'https://res.cloudinary.com/dg4tzo4pz/image/upload/v1723731105/spend_keeper/',

    # Add other endpoints as needed
}


cloudinary.config(
    cloud_name='dg4tzo4pz',
    api_key='273745232785925',
    api_secret='y6yndM6eBAVrLxSgXcl_ozdicXQ'
)
