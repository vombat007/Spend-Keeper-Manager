import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class RegistrationScreen(Screen):

    def register(self, instance):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if not email.strip() or not password.strip():
            self.ids.error_label.text = 'Please fill in all fields'
            return

        response = requests.post('http://127.0.0.1:8000/api/registration/', data={
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
