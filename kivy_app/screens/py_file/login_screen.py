import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.email_input = TextInput(hint_text='Email', multiline=False)
        layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        layout.add_widget(self.password_input)

        login_button = Button(text='Login', font_size=18, size_hint=(None, None), size=(200, 50))
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        back_button = Button(text='Back', font_size=18, size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        if not email.strip() or not password.strip():
            self.error_label.text = 'Please fill in all fields'
            return

        response = requests.post('http://127.0.0.1:8000/api/login/', data={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            self.error_label.text = 'Login successful'
            token = response.json().get('access')
            self.manager.get_screen('finance').set_token(token)
            self.manager.current = 'finance'
        else:
            self.error_label.text = 'Login failed: ' + response.text

    def go_back(self, instance):
        self.manager.current = 'home'
