from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy_app.config import ENDPOINTS
from PIL import Image, ImageOps
import requests
import os


class TransactionScreen(Screen):
    account_id = NumericProperty(1)
    account_name = StringProperty('Default Account')
    selected_type = StringProperty('Expense')
    selected_category = ObjectProperty(None)
    token = StringProperty('')

    def set_initial_type(self, trans_type):
        self.set_type(trans_type.capitalize())

    def on_pre_enter(self, *args):
        self.load_categories()

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

        filtered_categories = [cat for cat in categories if cat['type'].lower() == self.selected_type.lower()]

        for cat in filtered_categories:
            box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(70, 90))

            icon_path = f"kivy_app/assets/icon/{cat['type'].lower()}/{cat['icon']}"  # Construct the icon path

            # Create the image with a yellow border
            yellow_border_path = self.add_yellow_border(icon_path)

            btn = Button(
                text='',
                size_hint=(None, None),
                size=(70, 70),
                background_normal=icon_path,  # Set the button icon
                background_down=yellow_border_path  # Set the button icon with yellow border
            )
            btn.bind(on_press=self.on_category_button_press)
            btn.category_id = cat['id']

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

    def on_category_button_press(self, instance):
        self.selected_category = instance.category_id

        # Reset background of other buttons
        for button in self.ids.category_grid.children:
            if isinstance(button, BoxLayout):
                btn = button.children[1]  # Accessing the button inside the BoxLayout
                btn.background_normal = btn.background_down.replace('_selected', '')

        # Set the selected button background
        instance.background_normal = instance.background_down

    def go_back(self, instance):
        self.manager.current = 'home'

    def create_transaction(self):
        if not self.token:
            self.show_popup('Error', 'Token is missing. Please log in again.')
            return

        if not self.selected_category:
            self.show_popup('Error', 'Please select a valid category.')
            return

        headers = {'Authorization': f'Bearer {self.token}'}
        data = {
            'amount': self.ids.amount_input.text,
            'description': self.ids.description_input.text,
            'account': self.account_id,
            'category': self.selected_category
        }

        response = requests.post(ENDPOINTS['transactions'], headers=headers, data=data)
        if response.status_code == 201:
            self.show_popup('Success', 'Transaction created successfully!')
        else:
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

    def add_yellow_border(self, image_path):
        base_path, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)
        bordered_image_path = os.path.join(base_path, f"{name}_selected{ext}")

        if not os.path.exists(bordered_image_path):
            with Image.open(image_path) as img:
                border = ImageOps.expand(img, border=5, fill='yellow')
                border.save(bordered_image_path)

        return bordered_image_path
