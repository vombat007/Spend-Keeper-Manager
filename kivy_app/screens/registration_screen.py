import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        layout.add_widget(self.username_input)

        self.email_input = TextInput(hint_text='Email', multiline=False)
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        register_button = Button(text='Register', font_size=18, size_hint=(None, None), size=(200, 50))
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        self.error_label = Label(text='', color=(1, 0, 0, 1))

        back_button = Button(text='Back', font_size=18, size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not username.strip() or not email.strip() or not password.strip():
            self.error_label.text = 'Please fill in all fields'
            return

        response = requests.post('http://127.0.0.1:8000/api/registration/', data={
            'username': username,
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            self.error_label.text = 'Registration successful'
            self.manager.current = 'login'
        else:
            self.error_label.text = 'Registration failed: ' + response.text

    def go_back(self, instance):
        self.manager.current = 'home'
