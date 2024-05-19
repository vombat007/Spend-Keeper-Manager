import hashlib

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Username input
        self.username_input = TextInput(hint_text='Username')
        layout.add_widget(self.username_input)

        # Password input
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.password_input)

        # Login button
        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        # Error label (to display login error messages)
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        home_button = Button(text='Home')
        home_button.bind(on_press=self.go_to_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def login(self, instance):
        # Retrieve user input
        username = self.username_input.text
        password = self.password_input.text


    def go_to_home(self, instance):
        self.manager.current = 'home'
