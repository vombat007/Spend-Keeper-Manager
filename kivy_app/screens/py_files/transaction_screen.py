import requests
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class TransactionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.info_label = Label(text='Finance Info', font_size=18)

        layout.add_widget(self.info_label)

        self.add_widget(layout)

    def on_enter(self):
        self.fetch_accounts()

    def set_token(self, token):
        self.token = token

    def fetch_accounts(self):
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

    def go_back(self, instance):
        self.manager.current = 'home'
