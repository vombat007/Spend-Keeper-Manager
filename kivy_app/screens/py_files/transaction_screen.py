from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import requests
from kivy.app import App


class TransactionScreen(Screen):
    transaction_type = StringProperty('Income')  # Default to 'Income'
    amount = NumericProperty(0.0)
    description = StringProperty('')
    account_id = NumericProperty(1)  # Assuming the account_id is available
    category_data = {}  # Add category_data as an attribute

    def on_pre_enter(self, *args):
        self.load_categories()

    def load_categories(self):
        app = App.get_running_app()
        token = app.token
        if not token:
            self.show_popup('Error', 'Token is missing. Please log in again.')
            return

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('http://127.0.0.1:8000/api/categories/', headers=headers)
        if response.status_code == 200:
            categories = response.json()
            category_spinner = self.ids.category_spinner
            category_spinner.values = [f"{cat['name']} ({cat['type']})" for cat in categories]
            self.category_data = {f"{cat['name']} ({cat['type']})": cat for cat in categories}
        else:
            self.show_popup('Error', 'Failed to load categories')

    def go_back(self, instance):
        self.manager.current = 'home'

    def create_transaction(self):
        app = App.get_running_app()
        token = app.token  # Accessing token from FinancialApp instance
        if not token:
            self.show_popup('Error', 'Token is missing. Please log in again.')
            return

        selected_category = self.ids.category_spinner.text
        if selected_category not in self.category_data:
            self.show_popup('Error', 'Please select a valid category.')
            return

        category = self.category_data[selected_category]

        headers = {'Authorization': f'Bearer {token}'}
        data = {
            'amount': self.ids.amount_input.text,
            'description': self.ids.description_input.text,
            'account': self.account_id,
            'category': category['id']
        }

        response = requests.post('http://127.0.0.1:8000/api/transactions/', headers=headers, data=data)
        if response.status_code == 201:
            self.show_popup('Success', 'Transaction created successfully!')
        else:
            self.show_popup('Error', 'Failed to create transaction')

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.25))
        box.add_widget(btn)
        popup = Popup(title=title, content=box, size_hint=(0.8, 0.5))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def set_transaction_type(self, transaction_type):
        self.transaction_type = transaction_type
        self.ids.transaction_type_label.text = transaction_type
