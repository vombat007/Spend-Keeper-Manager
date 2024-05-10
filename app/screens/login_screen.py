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

        self.add_widget(layout)

    def login(self, instance):
        # Placeholder: Check if username and password are valid
        username = self.username_input.text
        password = self.password_input.text

        if username == 'admin' and password == 'password':
            self.error_label.text = 'Login successful!'
            # Add code to navigate to another screen (e.g., home screen)
        else:
            self.error_label.text = 'Invalid username or password'
