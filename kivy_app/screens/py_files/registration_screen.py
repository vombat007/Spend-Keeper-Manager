import requests
from kivy.uix.screenmanager import Screen
from config import ENDPOINTS


class RegistrationScreen(Screen):

    def register(self, instance):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if not email.strip() or not password.strip():
            self.ids.error_label.text = 'Please fill in all fields'
            return

        response = requests.post(ENDPOINTS['registration'], data={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            self.ids.error_label.text = 'Registration successful'
            self.manager.current = 'login'
        else:
            self.ids.error_label.text = 'Registration failed: ' + response.text

    def go_back(self, instance):
        self.manager.current = 'home'

    def signin(self, instance):
        self.manager.current = 'login'
