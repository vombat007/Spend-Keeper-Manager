import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class FinanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.info_label = Label(text='Finance Info')
        self.layout.add_widget(self.info_label)

        fetch_button = Button(text='Fetch Accounts')
        fetch_button.bind(on_press=self.fetch_accounts)
        self.layout.add_widget(fetch_button)

        home_button = Button(text='Home')
        home_button.bind(on_press=self.go_to_home)
        self.layout.add_widget(home_button)

    def set_token(self, token):
        self.token = token

    def fetch_accounts(self, instance):
        if not self.token:
            self.info_label.text = 'No token available'
            return

        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get('http://127.0.0.1:8000/api/accounts/', headers=headers)

        if response.status_code == 200:
            accounts = response.json()
            self.info_label.text = f'Accounts: {accounts}'
        else:
            self.info_label.text = 'Failed to fetch accounts: ' + response.text

    def go_to_home(self, instance):
        self.manager.current = 'home'
