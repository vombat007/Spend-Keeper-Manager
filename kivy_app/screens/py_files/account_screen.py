import json
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy_app.config import ENDPOINTS
from kivy.uix.dropdown import DropDown
from kivy_app.utils import TokenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.graphics import Color, RoundedRectangle, Line
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
        self.title_color = (0, 0, 0, 1)
        self.size_hint = (0.8, 0.3)
        self.background_color = (0, 0, 0, 0)  # Transparent background

        # Create the rounded white background rectangle
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Set background color to white
            self.rect = RoundedRectangle(
                radius=[(20, 20), (20, 20), (20, 20), (20, 20)],
                size=self.size,
                pos=self.pos
            )

        # Bind the size and position of the rectangle to the popup
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Add a black border using Line after the background is drawn
        with self.canvas.after:
            Color(0, 0, 0, 1)  # Set border color to black
            self.border_line = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, 20], width=2)

        layout = BoxLayout(orientation='vertical', padding=dp(20))

        # Custom input field with image background
        self.name_input = TextInput(
            hint_text="Account Name",
            foreground_color=(0, 0, 0, 1),  # Text color set to black
            background_normal='kivy_app/assets/img/Rectangle_Dash.png',
            background_active='kivy_app/assets/img/Rectangle_Dash.png',
            padding=[dp(25), dp(10)],  # Padding inside the text input to adjust text position
            cursor_color=(0, 0, 0, 1),  # Set the cursor color to black
            border=[0, 0, 0, 0],  # Remove border to prevent image stretching
        )
        layout.add_widget(self.name_input)

        # Add space between the input field and "Choose Currency" button
        layout.add_widget(Widget(size_hint_y=None, height=dp(10)))  # 20dp space between the input and button

        # Currency dropdown (custom image button)
        self.selected_currency = None
        self.currency_dropdown = DropDown()

        # Custom button with image for selecting currency
        self.currency_button = Button(
            text="Choose currency",
            size_hint_y=None,
            height=40,
            color=[0, 0, 0, 1],
            background_normal='kivy_app/assets/img/Rectangle_normal.png',  # Normal image
            background_down='kivy_app/assets/img/Rectangle_down.png',  # Pressed image
        )
        self.currency_button.bind(on_release=self.open_currency_dropdown)
        layout.add_widget(self.currency_button)

        # Add space between the two buttons
        layout.add_widget(Widget(size_hint_y=None, height=dp(5)))  # 20dp space between the buttons

        # Submit button (custom image button)
        submit_btn = Button(
            text="Create",
            size_hint_y=None,
            height=40,
            color=[0, 0, 0, 1],
            background_normal='kivy_app/assets/img/Rectangle_normal.png',
            background_down='kivy_app/assets/img/Rectangle_down.png',
        )
        submit_btn.bind(on_release=self.create_account)
        layout.add_widget(submit_btn)

        # Set the content of the popup to the layout
        self.content = layout

        # Fetch currencies after initializing layout
        self.fetch_currencies()

    def update_rect(self, *args):
        # Update the size and position of the rounded rectangle background
        self.rect.pos = self.pos
        self.rect.size = self.size

        # Update the black border position and size
        self.border_line.rounded_rectangle = [self.x, self.y, self.width, self.height, 20]

    def open_currency_dropdown(self, instance):
        """Open the currency dropdown when the button is clicked"""
        if not self.currency_dropdown.children:
            print("Dropdown is empty!")
        else:
            self.currency_dropdown.open(instance)

    def fetch_currencies(self):
        """Fetch available currencies from the API"""
        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}'}
        UrlRequest(
            url=ENDPOINTS['currencies'],
            on_success=self.populate_currencies,
            on_error=self.on_error,
            req_headers=headers
        )

    def populate_currencies(self, request, result):
        """Populate the currency dropdown with options"""
        self.currency_dropdown.clear_widgets()  # Clear any previous widgets
        for currency in result:
            # Create a button for each currency and add it to the dropdown
            btn = Button(
                text=f"{currency['name']} ({currency['symbol']})",
                size_hint_y=None,
                height=40,
                color=(0, 0, 0, 1)
            )
            btn.bind(on_release=lambda btn, currency=currency: self.select_currency(currency))
            self.currency_dropdown.add_widget(btn)

    def select_currency(self, currency):
        """Handle the selection of a currency"""
        self.currency_button.text = f"{currency['name']} ({currency['symbol']})"
        self.selected_currency = currency
        self.currency_dropdown.dismiss()

    def create_account(self, *args):
        """Create a new account with the selected currency"""
        account_name = self.name_input.text.strip()
        if not account_name or not self.selected_currency:
            print("Account name or currency not selected")
            return

        token = TokenManager.load_token()
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = json.dumps({
            'name': account_name,
            'currency': self.selected_currency['name']
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
        """Close the popup and refresh account data on success"""
        self.dismiss()
        self.parent_screen.fetch_account_data()

    def on_error(self, request, error):
        """Handle error fetching currencies"""
        print(f"Failed to fetch currencies: {error}")
