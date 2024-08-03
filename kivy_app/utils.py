import os
import json
import requests
from PIL import Image
from kivy_app.config import ENDPOINTS


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
