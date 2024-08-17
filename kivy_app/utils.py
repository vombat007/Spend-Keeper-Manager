import os
import json
import requests
from kivy_app.config import ENDPOINTS
from PIL import Image
import cloudinary
import cloudinary.api
import cloudinary.uploader
from datetime import datetime

cloudinary.config(
    cloud_name='dg4tzo4pz',
    api_key='273745232785925',
    api_secret='y6yndM6eBAVrLxSgXcl_ozdicXQ'
)


class TokenManager:
    token_file_path = 'tokens.json'

    @staticmethod
    def load_token():
        if os.path.exists(TokenManager.token_file_path):
            with open(TokenManager.token_file_path, 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('access')
        return None

    @staticmethod
    def load_refresh_token():
        if os.path.exists(TokenManager.token_file_path):
            with open(TokenManager.token_file_path, 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('refresh')
        return None

    @staticmethod
    def refresh_token():
        refresh_token = TokenManager.load_refresh_token()
        if refresh_token:
            response = requests.post(ENDPOINTS['refresh_token'], data={
                'refresh': refresh_token
            })
            if response.status_code == 200:
                new_tokens = response.json()
                with open(TokenManager.token_file_path, 'w') as token_file:
                    json.dump(new_tokens, token_file)
                return new_tokens['access']
            else:
                TokenManager.remove_tokens()
        return None

    @staticmethod
    def remove_tokens():
        if os.path.exists(TokenManager.token_file_path):
            os.remove(TokenManager.token_file_path)


def extract_frames(gif_path, output_folder):
    with Image.open(gif_path) as img:
        for i in range(img.n_frames):
            img.seek(i)
            img.save(os.path.join(output_folder, f"frame_{i}.png"))


def download_image(url):
    # Ensure the directory exists
    local_dir = os.path.join('kivy_app', 'assets', 'icon')
    os.makedirs(local_dir, exist_ok=True)

    # Create a local file path
    filename = url.split('/')[-1]
    local_path = os.path.join(local_dir, filename)

    # Download and save the image if it doesn't already exist
    if not os.path.exists(local_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)

    return local_path


def download_all_icons_from_cloudinary(local_base_dir):
    # Create base directory if it doesn't exist
    os.makedirs(local_base_dir, exist_ok=True)

    # Fetch list of resources in Cloudinary folder
    resources = cloudinary.api.resources(type='upload', prefix='spend_keeper/all_category_icon/', max_results=500)

    for resource in resources.get('resources', []):
        # Extract the secure URL and original filename
        secure_url = resource['secure_url']
        original_filename = secure_url.split('/')[-1]  # Extract the filename from the URL

        # Determine the local directory and file path
        relative_path = resource['public_id'].replace('spend_keeper/all_category_icon/',
                                                      '')  # Remove the Cloudinary base prefix
        local_dir = os.path.join(local_base_dir, os.path.dirname(relative_path))
        os.makedirs(local_dir, exist_ok=True)  # Ensure the directory exists

        local_file_path = os.path.join(local_dir, original_filename)  # Use the original filename

        # Convert the Cloudinary `created_at` timestamp to a Unix timestamp
        cloudinary_created_at = datetime.strptime(resource['created_at'],
                                                  "%Y-%m-%dT%H:%M:%S%z").timestamp()

        # Download and save the file if it doesn't exist or is outdated
        if not os.path.exists(local_file_path) or os.path.getmtime(local_file_path) < cloudinary_created_at:
            response = requests.get(secure_url)
            if response.status_code == 200:
                with open(local_file_path, 'wb') as file:
                    file.write(response.content)
            print(f"Downloaded {local_file_path}")
