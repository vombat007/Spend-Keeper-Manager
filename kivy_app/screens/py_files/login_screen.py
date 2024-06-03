import requests
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def login(self, instance):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if not email.strip() or not password.strip():
            self.ids.error_label.text = 'Please fill in all fields'
            return

        response = requests.post('http://127.0.0.1:8000/api/login/', data={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            self.ids.error_label.text = 'Login successful'
            token = response.json().get('access')
            self.manager.get_screen('finance').set_token(token)
            self.manager.current = 'finance'
        else:
            self.ids.error_label.text = 'Login failed: ' + response.text

    def go_back(self, instance):
        self.manager.current = 'home'

    def forgot_password(self, instance):
        # Implement forgot password logic
        pass

    def signup(self, instance):
        # Implement signup logic
        pass
