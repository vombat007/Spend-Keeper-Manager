import json
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy_app.config import ENDPOINTS
from kivy.uix.dropdown import DropDown
from kivy_app.utils import TokenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, ListProperty


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
        self.size_hint = (0.8, 0.6)

        layout = BoxLayout(orientation='vertical')

        # Account name input
        self.name_input = TextInput(hint_text="Account Name")
        layout.add_widget(self.name_input)

        # Currency dropdown
        self.selected_currency = None
        self.currency_dropdown = DropDown()
        self.currency_button = Button(text="Select Currency", size_hint_y=None, height=40)
        self.currency_button.bind(on_release=self.currency_dropdown.open)
        layout.add_widget(self.currency_button)

        self.fetch_currencies()

        submit_btn = Button(text="Create", size_hint_y=None, height=40)
        submit_btn.bind(on_release=self.create_account)
        layout.add_widget(submit_btn)

        self.content = layout

    def fetch_currencies(self):
        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}'}
        UrlRequest(
            url=ENDPOINTS['currencies'],
            on_success=self.populate_currencies,
            on_error=self.on_error,
            req_headers=headers
        )

    def populate_currencies(self, request, result):
        for currency in result:
            btn = Button(text=f"{currency['name']} ({currency['symbol']})", size_hint_y=None, height=40)
            # Pass the currency object directly so we can access its ID
            btn.bind(on_release=lambda btn, currency=currency: self.select_currency(currency))
            self.currency_dropdown.add_widget(btn)

    def select_currency(self, currency):
        # Set the button text to the selected currency's name and symbol
        self.currency_button.text = f"{currency['name']} ({currency['symbol']})"
        # Store the selected currency object for use in account creation
        self.selected_currency = currency
        # Close the dropdown
        self.currency_dropdown.dismiss()

    def create_account(self, *args):
        account_name = self.name_input.text.strip()
        if not account_name or not self.selected_currency:
            print("Account name or currency not selected")
            return

        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = json.dumps({
            'name': account_name,
            'currency': self.selected_currency['name']  # Or use 'id': self.selected_currency['id'] if backend uses ID
        })

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
