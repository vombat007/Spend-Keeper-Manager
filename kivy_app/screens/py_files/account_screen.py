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

        # Ensure the dropdown is initialized
        self.currency_dropdown = DropDown()

        # Disable the default background image and set it to transparent for custom drawing
        self.background = 'kivy_app/assets/img/Rounded_square.png'  # Disable the default background
        self.background_color = (1, 1, 1, 1)  # Fully transparent to allow custom background

        # Use canvas to draw the rounded background and the black border
        with self.canvas.before:
            # White background with rounded corners
            Color(1, 1, 1, 1)  # White background color (R, G, B, A)
            self.rect = RoundedRectangle(
                radius=[20, 20, 20, 20],  # Rounded corners
                size=self.size,
                pos=self.pos
            )

        # Bind the size and position updates of the background to the popup's size and position
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Draw a black rounded border around the popup
        with self.canvas.after:
            Color(0, 0, 0, 1)  # Black color for the border
            self.border_line = Line(
                rounded_rectangle=[self.x, self.y, self.width, self.height, 20],  # Same rounded corners
                width=2  # Border width
            )

        # Create the layout for the popup content
        layout = BoxLayout(orientation='vertical', padding=dp(20))

        # Account name input
        self.name_input = TextInput(
            hint_text="Account Name",
            foreground_color=(0, 0, 0, 1),
            background_normal='kivy_app/assets/img/Rectangle_Dash.png',
            background_active='kivy_app/assets/img/Rectangle_Dash.png',
            padding=[dp(25), dp(10)],
            cursor_color=(0, 0, 0, 1),
            border=[0, 0, 0, 0]
        )
        layout.add_widget(self.name_input)

        layout.add_widget(Widget(size_hint_y=None, height=dp(20)))  # Add space

        # Currency button
        self.currency_button = Button(
            text="Choose currency",
            size_hint_y=None,
            height=40,
            color=[0, 0, 0, 1],
            background_normal='kivy_app/assets/img/Rectangle_normal.png',
            background_down='kivy_app/assets/img/Rectangle_down.png',
        )
        self.currency_button.bind(on_release=self.open_currency_dropdown)
        layout.add_widget(self.currency_button)

        layout.add_widget(Widget(size_hint_y=None, height=dp(5)))  # Add space

        # Submit button
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
        """Update the size and position of the rounded rectangle background and border."""
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border_line.rounded_rectangle = [self.x, self.y, self.width, self.height, 20]

    def populate_currencies(self, request, result):
        """Populate the currency dropdown with options."""
        # Ensure currency_dropdown is initialized
        if not hasattr(self, 'currency_dropdown') or self.currency_dropdown is None:
            self.currency_dropdown = DropDown()

        # Clear any previous widgets
        self.currency_dropdown.clear_widgets()

        # Create a BoxLayout to hold the buttons with spacing
        button_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None)

        # Adjust the height dynamically based on the number of buttons
        button_layout.height = len(result) * (40 + 5)  # Button height + spacing

        for currency in result:
            btn = Button(
                text=f"{currency['name']} ({currency['symbol']})",
                size_hint_y=None,
                height=40,
                color=(0, 0, 0, 1),
                background_normal='',  # Disable the default background
                background_color=(0, 0, 0, 0)  # Transparent to allow custom canvas drawing
            )

            # Use canvas to draw the rounded rectangle and border for each button
            with btn.canvas.before:
                Color(1, 1, 1, 1)  # White background
                btn.rect = RoundedRectangle(
                    size=btn.size,
                    pos=btn.pos,
                    radius=[dp(20), dp(20), dp(20), dp(20)]  # Rounded corners
                )

            with btn.canvas.after:
                Color(0, 0, 0, 1)  # Black color for the border
                btn.border_line = Line(
                    rounded_rectangle=[btn.x, btn.y, btn.width, btn.height, 20],  # Border with rounded corners
                    width=1.5  # Border width
                )

            # Bind size and position updates
            btn.bind(size=self.update_button_canvas, pos=self.update_button_canvas)

            # Bind button to select currency
            btn.bind(on_release=lambda btn, currency=currency: self.select_currency(currency))

            # Add the button to the layout
            button_layout.add_widget(btn)

        # Add the button layout to the dropdown
        self.currency_dropdown.add_widget(button_layout)

    @staticmethod
    def update_button_canvas(instance, *args):
        """Update the size and position of the rounded rectangle background and border."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
        instance.border_line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 20]

    def open_currency_dropdown(self, instance):
        """Open the currency dropdown when the button is clicked."""
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
