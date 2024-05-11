from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Button to navigate to finance screen
        finance_button = Button(text='Finance Screen')
        finance_button.bind(on_press=self.go_to_finance)
        layout.add_widget(finance_button)

        registration_button = Button(text='Registration Screen')
        registration_button.bind(on_press=self.go_to_registration)
        layout.add_widget(registration_button)

        login_button = Button(text='Login Screen')
        login_button.bind(on_press=self.go_to_login)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def go_to_finance(self, instance):
        self.manager.current = 'finance'

    def go_to_registration(self, instance):
        self.manager.current = 'registration'

    def go_to_login(self, instance):
        self.manager.current = 'login'
