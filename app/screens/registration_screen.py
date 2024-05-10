from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.registered_users = {}  # Store registered users

        layout = BoxLayout(orientation='vertical')

        # Username input
        self.username_input = TextInput(hint_text='Username')
        layout.add_widget(self.username_input)

        # Email input
        self.email_input = TextInput(hint_text='Email')
        layout.add_widget(self.email_input)

        # Password input
        self.password_input = TextInput(hint_text='Password', password=True)
        layout.add_widget(self.password_input)

        # Register button
        register_button = Button(text='Register')
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        # Error label (to display registration error messages)
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        home_button = Button(text='Home')
        home_button.bind(on_press=self.go_to_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def register(self, instance):
        # Placeholder: Check if registration inputs are valid
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        # Placeholder: Check if username and email are not empty and if password is at least 6 characters long
        if username.strip() and email.strip() and len(password) >= 6:
            # Store the registered user
            self.registered_users[username] = {'email': email, 'password': password}
            self.error_label.text = 'Registration successful!'
            # Add code to navigate to another screen (e.g., login screen)
            self.manager.current = 'login'
        else:
            self.error_label.text = 'Invalid registration details'

    def go_to_home(self, instance):
        self.manager.current = 'home'
