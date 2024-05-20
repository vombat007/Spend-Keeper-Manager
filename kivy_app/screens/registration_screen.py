import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        self.username_input = TextInput(hint_text='Username')
        layout.add_widget(self.username_input)

        self.email_input = TextInput(hint_text='Email')
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.password_input)

        register_button = Button(text='Register')
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        home_button = Button(text='Home')
        home_button.bind(on_press=self.go_to_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not username.strip() or not email.strip() or not password.strip():
            self.error_label.text = 'Please fill in all fields'
            return

        # Sending a registration request to the Django API
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

    def go_to_home(self, instance):
        self.manager.current = 'home'
