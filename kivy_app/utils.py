import os
import json
import requests
from PIL import Image


class TokenManager:
    @staticmethod
    def load_token():
        if os.path.exists('tokens.json'):
            with open('tokens.json', 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('access')
        return None

    @staticmethod
    def refresh_token():
        if os.path.exists('tokens.json'):
            with open('tokens.json', 'r') as token_file:
                tokens = json.load(token_file)
                refresh_token = tokens.get('refresh')
                response = requests.post('http://127.0.0.1:8000/api/login/refresh/', data={
                    'refresh': refresh_token
                })
                if response.status_code == 200:
                    new_tokens = response.json()
                    with open('tokens.json', 'w') as token_file:
                        json.dump(new_tokens, token_file)
                    return new_tokens['access']
                else:
                    os.remove('tokens.json')
        return None


def extract_frames(gif_path, output_folder):
    with Image.open(gif_path) as img:
        for i in range(img.n_frames):
            img.seek(i)
            img.save(os.path.join(output_folder, f"frame_{i}.png"))
