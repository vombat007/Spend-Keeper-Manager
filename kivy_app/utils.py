import os
import json
import requests
from kivy_app.config import ENDPOINTS
from PIL import Image
from datetime import datetime
import cloudinary.api


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


def download_image(icon_name, category_type, is_custom=False):
    """
    Downloads the image from either default or custom location.

    Args:
        icon_name (str): The name of the icon file.
        category_type (str): The type of the category, e.g., 'expense' or 'income'.
        is_custom (bool): Flag to indicate if the icon is custom.

    Returns:
        str: The local path to the downloaded image.
    """
    if is_custom:
        local_dir = os.path.join('kivy_app', 'assets', 'icon', 'custom_category_icons')
    else:
        local_dir = os.path.join('kivy_app', 'assets', 'icon', 'default_icons', category_type)

    # Ensure the directory exists
    os.makedirs(local_dir, exist_ok=True)

    # Create a local file path
    local_path = os.path.join(local_dir, icon_name)

    # Download and save the image if it doesn't already exist
    if not os.path.exists(local_path):
        if is_custom:
            # Download from Cloudinary if custom icon
            cloudinary_url = ENDPOINTS['custom_icon'] + f"{icon_name}"
        else:
            # Default icon URL
            cloudinary_url = ENDPOINTS['default_icon'] + f"{category_type}/{icon_name}"

        response = requests.get(cloudinary_url)
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
        secure_url = resource['secure_url']
        # Ensure the file is saved with a .png extension
        local_file_path = os.path.join(local_base_dir,
                                       resource['public_id'].replace('spend_keeper/all_category_icon/', '') + '.png')

        # Ensure the directory exists
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

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
