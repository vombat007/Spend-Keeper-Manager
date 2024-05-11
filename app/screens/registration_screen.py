import hashlib
import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from app.databases.development import get_connection


class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        # Retrieve user input
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        # Validate user input (add more validation as needed)
        if not username.strip() or not email.strip() or not password.strip():
            self.error_label.text = 'Please fill in all fields'
            return

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert user data into the database
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
            self.error_label.text = 'Registration successful!'

            self.manager.current = 'login'

        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                self.error_label.text = 'Username or email already exists'
            else:
                self.error_label.text = 'Registration failed'
        finally:
            conn.close()

    def go_to_home(self, instance):
        self.manager.current = 'home'
