import requests
from kivy.uix.screenmanager import Screen
import json
from kivy_app.config import ENDPOINTS


class LoginScreen(Screen):
    def login(self, instance):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if not email.strip() or not password.strip():
            self.ids.error_label.text = 'Please fill in all fields'
            return

        response = requests.post(ENDPOINTS['login'], data={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            self.ids.error_label.text = 'Login successful'
            tokens = response.json()
            with open('tokens.json', 'w') as token_file:
                json.dump(tokens, token_file)
            home_screen = self.manager.get_screen('home')
            home_screen.token = tokens.get('access')
            home_screen.fetch_accounts()
            self.manager.current = 'home'
        else:
            self.ids.error_label.text = 'Login failed: ' + response.text

    def go_back(self, instance):
        self.manager.current = 'start'

    def forgot_password(self, instance):
        # Implement forgot password logic
        pass

    def sign_up(self, instance):
        self.manager.current = 'registration'
