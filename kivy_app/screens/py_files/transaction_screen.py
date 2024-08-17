import json
import logging
import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Line
from kivy_app.config import ENDPOINTS
from datetime import datetime, timedelta
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy_app.utils import download_image
from kivy_app.widget.date_picker_app import DatePicker
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

logger = logging.getLogger(__name__)


class TransactionScreen(Screen):
    account_id = NumericProperty(1)
    account_name = StringProperty('Default Account')
    selected_type = StringProperty('Expense')
    selected_category = ObjectProperty(None)
    token = StringProperty('')
    selected_date = StringProperty(datetime.now().strftime('%Y-%m-%d'))
    current_date = datetime.now()

    def set_initial_type(self, trans_type):
        self.set_type(trans_type.capitalize())

    def on_pre_enter(self, *args):
        self.load_categories()
        self.update_period_label()
        self.update_button_visibility()

    def load_categories(self):
        if not self.token:
            self.show_popup('Error', 'Token is missing. Please log in again.')
            return

        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(ENDPOINTS['categories'], headers=headers)
        if response.status_code == 200:
            categories = response.json()
            self.display_categories(categories)
        else:
            self.show_popup('Error', 'Failed to load categories')

    def display_categories(self, categories):
        grid = self.ids.category_grid
        grid.clear_widgets()

        filtered_categories = [
            {
                'id': cat['id'],
                'name': cat['name'],
                'type': cat['type'],
                'icon': '/'.join(cat['icon'].split('/')[-1:])  # Extract only the last one parts
            }
            for cat in categories
            if cat['type'].lower() == self.selected_type.lower()
        ]

        for cat in filtered_categories:
            box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(70, 90))

            # Construct the icon URL using Cloudinary's structure
            icon_url = (ENDPOINTS['icon_url'] + f"{cat['type'].lower()}/{cat['icon']}.png")

            # Download the image
            icon_path = download_image(icon_url)

            # Create the button with the downloaded image
            btn = Button(
                text='',
                size_hint=(None, None),
                size=(70, 70),
                background_normal=icon_path,
                background_down=icon_path
            )
            btn.bind(on_press=self.on_category_button_press)
            btn.category_id = cat['id']

            # Bind to update the border when the button size or position changes
            btn.bind(pos=self.update_border, size=self.update_border)

            label = Label(
                text=cat['name'],
                font_name='kivy_app/assets/fonts/IrishGrover-Regular.ttf',
                size_hint=(None, None),
                size=(70, 20),
                font_size=12,
                color=(0, 0, 0, 1),
                halign='center',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))

            box.add_widget(btn)
            box.add_widget(label)
            grid.add_widget(box)

        # Add the "Create" button at the end
        create_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(70, 90))
        create_btn = Button(
            size_hint=(None, None),
            size=(70, 70),
            background_normal='kivy_app/assets/icon/create_icon.png',  # Path for the create button icon
            background_down='kivy_app/assets/icon/create_icon.png'
        )
        create_btn.bind(on_press=self.create_category)

        create_label = Label(
            text='Create',
            font_name='kivy_app/assets/fonts/IrishGrover-Regular.ttf',
            size_hint=(None, None),
            size=(70, 20),
            font_size=12,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        create_label.bind(size=create_label.setter('text_size'))

        create_box.add_widget(create_btn)
        create_box.add_widget(create_label)
        grid.add_widget(create_box)

    def update_border(self, instance, value):
        # If borders exist, update their position and size
        if hasattr(instance, 'outer_border') and hasattr(instance, 'inner_border'):
            instance.outer_border.rounded_rectangle = (
                instance.x, instance.y, instance.width, instance.height, 20
            )
            instance.inner_border.rounded_rectangle = (
                instance.x + 5, instance.y + 5, instance.width - 10, instance.height - 10, 15
            )

    def on_category_button_press(self, instance):
        self.selected_category = instance.category_id

        # Reset background and borders of other buttons
        for button in self.ids.category_grid.children:
            if isinstance(button, BoxLayout):
                btn = button.children[1]  # Accessing the button inside the BoxLayout
                # Clear the canvas for non-selected buttons
                btn.canvas.after.clear()
                # Remove border attributes to avoid updating non-existing borders
                if hasattr(btn, 'outer_border'):
                    del btn.outer_border
                if hasattr(btn, 'inner_border'):
                    del btn.inner_border

        # Set the selected button background and show the yellow and black borders
        with instance.canvas.after:
            # Yellow outer border
            Color(1, 1, 0, 1)  # Yellow color
            instance.outer_border = Line(
                width=4,
                rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 20)
            )

            # Black inner border
            Color(0, 0, 0, 1)  # Black color
            instance.inner_border = Line(
                width=1,
                rounded_rectangle=(instance.x + 5, instance.y + 5, instance.width - 10, instance.height - 10, 15)
            )

    def go_back(self, instance):
        self.manager.current = 'home'

    def go_calculator(self, instance):
        self.manager.current = 'calculator'

    def create_transaction(self):
        if not self.token:
            self.show_popup('Error', 'Token is missing. Please log in again.')
            return

        if not self.selected_category:
            self.show_popup('Error', 'Please select a valid category.')
            return

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {
            'amount': self.ids.amount_input.text,
            'note': self.ids.description_input.text,
            'account': self.account_id,
            'category': self.selected_category,
            'datetime': self.selected_date  # Ensure the selected date is included in the data
        }

        response = requests.post(ENDPOINTS['transactions'], headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            self.show_popup('Success', 'Transaction created successfully!')
        else:
            logger.error("Failed to create transaction: %s", response.content)
            self.show_popup('Error', 'Failed to create transaction')

    @staticmethod
    def show_popup(title, message):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.25))
        box.add_widget(btn)
        popup = Popup(title=title, content=box, size_hint=(0.8, 0.5))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def set_type(self, trans_type):
        self.selected_type = trans_type
        if trans_type == 'Income':
            self.ids.income_button.state = 'down'
            self.ids.expense_button.state = 'normal'
            self.ids.income_button.background_normal = self.ids.income_button.background_down
            self.ids.expense_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'
        else:
            self.ids.income_button.state = 'normal'
            self.ids.expense_button.state = 'down'
            self.ids.expense_button.background_normal = self.ids.expense_button.background_down
            self.ids.income_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'
        self.load_categories()

    def open_date_picker(self):
        date_picker = DatePicker()
        date_picker.bind(on_date=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance, value):
        if value <= datetime.now().date():
            self.selected_date = value.strftime('%Y-%m-%d')
            self.ids.period_label_id.text = self.selected_date
        else:
            self.show_popup('Invalid Date', 'Please select today or a past date.')

    def change_period(self, direction):
        new_date = self.current_date + timedelta(days=direction)
        if new_date <= datetime.now():
            self.current_date = new_date
            self.selected_date = self.current_date.strftime('%Y-%m-%d')
            self.ids.period_label_id.text = self.selected_date
            self.update_button_visibility()
        else:
            self.show_popup('Invalid Date', 'Cannot set a date in the future.')

    def update_button_visibility(self):
        now = datetime.now().date()

        left_button = self.ids.left_arrow_button
        right_button = self.ids.right_arrow_button

        left_button.disabled = self.current_date.date() <= datetime(2000, 1, 1).date()
        right_button.disabled = self.current_date.date() >= now

    def update_period_label(self):
        self.ids.period_label_id.text = self.selected_date

    def create_category(self, instance):
        # Store the selected transaction type
        self.manager.get_screen('create_category').set_initial_type(self.selected_type)
        self.manager.current = 'create_category'
