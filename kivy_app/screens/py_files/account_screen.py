import json

from kivy.properties import StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy_app.config import ENDPOINTS
from kivy_app.utils import TokenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest


class AccountItem(BoxLayout):
    text = StringProperty("")
    color = ListProperty([0, 0, 0, 1])


class AccountScreen(Screen):

    def on_enter(self, *args):
        self.fetch_account_data()

    def fetch_account_data(self):
        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}'}
        UrlRequest(
            url=ENDPOINTS['accounts'],
            on_success=self.display_accounts,
            on_error=self.on_error,
            req_headers=headers
        )

    def display_accounts(self, request, result):
        data = []
        for account in result:
            account_name = account['name']
            account_balance = account['total_balance']
            data.append(
                {'text': f"{account_name}: ${account_balance}",
                 'color': (0, 0, 0, 1)})

        # Update the RecycleView data
        self.ids.account_list.data = data

    def on_error(self, request, error):
        print(f"Failed to fetch accounts: {error}")

    def open_create_account_popup(self):
        popup = CreateAccountPopup(self)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'home'


class CreateAccountPopup(Popup):
    def __init__(self, parent_screen, **kwargs):
        super(CreateAccountPopup, self).__init__(**kwargs)
        self.parent_screen = parent_screen
        self.title = "Create New Account"
        self.size_hint = (0.8, 0.5)

        layout = BoxLayout(orientation='vertical')

        self.name_input = TextInput(hint_text="Account Name")
        layout.add_widget(self.name_input)

        submit_btn = Button(text="Create", size_hint_y=None, height=40)
        submit_btn.bind(on_release=self.create_account)
        layout.add_widget(submit_btn)

        self.content = layout

    def create_account(self, *args):
        account_name = self.name_input.text.strip()
        if not account_name:
            return

        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = json.dumps({'name': account_name})

        UrlRequest(
            url=ENDPOINTS['accounts'],
            req_body=data,
            req_headers=headers,
            method='POST',
            on_success=self.on_success,
            on_error=self.on_error
        )

    def on_success(self, request, result):
        self.dismiss()
        self.parent_screen.fetch_account_data()

    def on_error(self, request, error):
        print(f"Failed to create account: {error}")
