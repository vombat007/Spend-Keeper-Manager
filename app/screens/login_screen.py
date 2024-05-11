import hashlib

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from app.databases.development import get_connection


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

        # Validate user input (add more validation as needed)
        if not username.strip() or not password.strip():
            self.error_label.text = 'Please fill in all fields'
            return

        # Hash the password input by the user
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if username exists in the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            # If the username exists, compare the hashed password with the password stored in the database
            if user[3] == hashed_password:  # Index 3 corresponds to the hashed password column
                self.error_label.text = 'Login successful!'
                self.manager.current = 'home'
            else:
                self.error_label.text = 'Invalid password'
        else:
            self.error_label.text = 'Invalid username'

        conn.close()

    def go_to_home(self, instance):
        self.manager.current = 'home'
