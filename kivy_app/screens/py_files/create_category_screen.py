import os
import requests
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy_app.config import ENDPOINTS
from kivy_app.utils import TokenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, Ellipse, RoundedRectangle


class ColorCircleButton(ButtonBehavior, Widget):
    def __init__(self, color, **kwargs):
        super(ColorCircleButton, self).__init__(**kwargs)
        self.color = color
        self.size_hint = (None, None)
        self.size = (dp(25), dp(25))
        with self.canvas:
            Color(*self.color)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_ellipse, size=self.update_ellipse)

    def update_ellipse(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size


class CreateCategoryScreen(Screen):
    selected_icon = StringProperty('')
    selected_color = ListProperty([1, 1, 1, 1])
    category_name = StringProperty('')

    def on_pre_enter(self, *args):

        self.display_icons()
        self.display_color_options()
        self.toggle_display('icon')  # Default to showing icons
        self.update_type_buttons()  # Update the buttons based on the selected type

    def set_initial_type(self, trans_type):
        self.selected_type = trans_type.capitalize()

    def update_type_buttons(self):
        """Update the button states based on the selected type."""
        if self.selected_type == 'Income':
            self.ids.income_button.state = 'down'
            self.ids.expense_button.state = 'normal'
            self.ids.income_button.background_normal = self.ids.income_button.background_down
            self.ids.expense_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'
        else:
            self.ids.income_button.state = 'normal'
            self.ids.expense_button.state = 'down'
            self.ids.expense_button.background_normal = self.ids.expense_button.background_down
            self.ids.income_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'

    def on_income_button_press(self):
        """Handle the press of the Income button."""
        self.selected_type = 'Income'
        self.update_type_buttons()

    def on_expense_button_press(self):
        """Handle the press of the Expense button."""
        self.selected_type = 'Expense'
        self.update_type_buttons()

    def go_back(self, instance):
        self.manager.current = 'transaction'

    def display_icons(self):
        icon_grid = self.ids.icon_grid
        icon_grid.clear_widgets()
        icon_path = 'kivy_app/assets/icon/all/'

        for folder_name in os.listdir(icon_path):
            folder_path = os.path.join(icon_path, folder_name)
            if os.path.isdir(folder_path):
                folder_label = Label(
                    text=folder_name,
                    font_name='kivy_app/assets/fonts/IrishGrover-Regular.ttf',
                    size_hint_y=None,
                    height=dp(50),
                    font_size=dp(24),
                    halign='center',
                    valign='middle',
                    color=(0, 0, 0, 1)
                )
                folder_label.bind(size=folder_label.setter('text_size'))
                icon_grid.add_widget(folder_label)

                icons_layout = GridLayout(cols=5, spacing=dp(10), size_hint_y=None)
                icons_layout.bind(minimum_height=icons_layout.setter('height'))

                for icon_file in os.listdir(folder_path):
                    if icon_file.endswith('.png'):
                        btn = Button(
                            size_hint=(None, None),
                            size=(dp(64), dp(64)),
                            background_normal=os.path.join(folder_path, icon_file),
                            background_down=os.path.join(folder_path, icon_file)
                        )
                        btn.bind(on_press=self.select_icon)
                        btn.icon_path = os.path.join(folder_path, icon_file)
                        icons_layout.add_widget(btn)

                icon_grid.add_widget(icons_layout)

    def select_icon(self, instance):
        self.selected_icon = instance.icon_path
        self.update_selected_icon()

    def update_selected_icon(self):
        if self.selected_icon:
            self.ids.selected_icon_display.canvas.before.clear()
            with self.ids.selected_icon_display.canvas.before:
                Color(*self.selected_color)
                RoundedRectangle(pos=self.ids.selected_icon_display.pos,
                                 size=self.ids.selected_icon_display.size,
                                 radius=[20, 20, 20, 20])
                Color(1, 1, 1, 1)
                RoundedRectangle(source=self.selected_icon,
                                 pos=self.ids.selected_icon_display.pos,
                                 size=self.ids.selected_icon_display.size,
                                 radius=[20, 20, 20, 20])

    def display_color_options(self):
        color_grid = self.ids.color_grid
        color_grid.clear_widgets()

        color_choices = [
            # Red gradient
            [1.0, 0.0, 0.0, 1.0],  # Bright Red
            [0.9, 0.0, 0.0, 1.0],
            [0.8, 0.0, 0.0, 1.0],
            [0.7, 0.0, 0.0, 1.0],
            [0.6, 0.0, 0.0, 1.0],
            [0.5, 0.0, 0.0, 1.0],
            [0.4, 0.0, 0.0, 1.0],  # Pale Red

            # Green gradient
            [0.0, 1.0, 0.0, 1.0],  # Bright Green
            [0.0, 0.9, 0.0, 1.0],
            [0.0, 0.8, 0.0, 1.0],
            [0.0, 0.7, 0.0, 1.0],
            [0.0, 0.6, 0.0, 1.0],
            [0.0, 0.5, 0.0, 1.0],
            [0.0, 0.4, 0.0, 1.0],  # Pale Green

            # Blue gradient
            [0.0, 0.0, 1.0, 1.0],  # Bright Blue
            [0.0, 0.0, 0.9, 1.0],
            [0.0, 0.0, 0.8, 1.0],
            [0.0, 0.0, 0.7, 1.0],
            [0.0, 0.0, 0.6, 1.0],
            [0.0, 0.0, 0.5, 1.0],
            [0.0, 0.0, 0.4, 1.0],  # Pale Blue

            # Yellow gradient
            [1.0, 1.0, 0.0, 1.0],  # Bright Yellow
            [0.9, 0.9, 0.0, 1.0],
            [0.8, 0.8, 0.0, 1.0],
            [0.7, 0.7, 0.0, 1.0],
            [0.6, 0.6, 0.0, 1.0],
            [0.5, 0.5, 0.0, 1.0],
            [0.4, 0.4, 0.0, 1.0],  # Pale Yellow

            # Orange gradient
            [1.0, 0.5, 0.0, 1.0],  # Bright Orange
            [0.9, 0.45, 0.0, 1.0],
            [0.8, 0.4, 0.0, 1.0],
            [0.7, 0.35, 0.0, 1.0],
            [0.6, 0.3, 0.0, 1.0],
            [0.5, 0.25, 0.0, 1.0],
            [0.4, 0.2, 0.0, 1.0],  # Pale Orange

            # Purple gradient
            [0.5, 0.0, 0.5, 1.0],  # Bright Purple
            [0.45, 0.0, 0.45, 1.0],
            [0.4, 0.0, 0.4, 1.0],
            [0.35, 0.0, 0.35, 1.0],
            [0.3, 0.0, 0.3, 1.0],
            [0.25, 0.0, 0.25, 1.0],
            [0.2, 0.0, 0.2, 1.0],  # Pale Purple

            # Cyan gradient
            [0.0, 1.0, 1.0, 1.0],  # Bright Cyan
            [0.0, 0.9, 0.9, 1.0],
            [0.0, 0.8, 0.8, 1.0],
            [0.0, 0.7, 0.7, 1.0],
            [0.0, 0.6, 0.6, 1.0],
            [0.0, 0.5, 0.5, 1.0],
            [0.0, 0.4, 0.4, 1.0],  # Pale Cyan

            # Magenta gradient
            [1.0, 0.0, 1.0, 1.0],  # Bright Magenta
            [0.9, 0.0, 0.9, 1.0],
            [0.8, 0.0, 0.8, 1.0],
            [0.7, 0.0, 0.7, 1.0],
            [0.6, 0.0, 0.6, 1.0],
            [0.5, 0.0, 0.5, 1.0],
            [0.4, 0.0, 0.4, 1.0],  # Pale Magenta

            # Brown gradient (replacing Black)
            [0.6, 0.3, 0.0, 1.0],  # Bright Brown
            [0.55, 0.275, 0.0, 1.0],
            [0.5, 0.25, 0.0, 1.0],
            [0.45, 0.225, 0.0, 1.0],
            [0.4, 0.2, 0.0, 1.0],
            [0.35, 0.175, 0.0, 1.0],
            [0.3, 0.15, 0.0, 1.0],  # Pale Brown

            # Pink gradient (added new color)
            [1.0, 0.75, 0.8, 1.0],  # Bright Pink
            [0.9, 0.675, 0.72, 1.0],
            [0.8, 0.6, 0.64, 1.0],
            [0.7, 0.525, 0.56, 1.0],
            [0.6, 0.45, 0.48, 1.0],
            [0.5, 0.375, 0.4, 1.0],
            [0.4, 0.3, 0.32, 1.0],  # Pale Pink
        ]

        for color in color_choices:
            btn = ColorCircleButton(color=color)
            btn.bind(on_press=lambda instance, color=color: self.select_color(instance, color))
            color_grid.add_widget(btn)

    def select_color(self, instance, color):
        self.selected_color = color
        self.update_selected_icon()

    def capture_widget_to_image(self, widget, save_dir):
        """Capture the widget canvas to an image file."""
        image = widget.export_as_image()
        file_path = os.path.join(save_dir, f"{self.category_name}.png")
        image.save(file_path)
        return file_path

    def create_category(self):
        if not self.category_name or not self.selected_icon:
            self.show_popup('Error', 'Please provide all the details.')
            return

        # Directory where custom icons are saved locally
        save_dir = 'kivy_app/assets/icon/custom_category_icons/'

        # Create the directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Schedule the capture and upload slightly after rendering
        Clock.schedule_once(lambda dt:
                            self.capture_and_upload_icon(
                                self.ids.selected_icon_display, save_dir))

    def capture_and_upload_icon(self, widget, save_dir):
        # Capture the widget to an image
        local_file_path = self.capture_widget_to_image(widget, save_dir)

        # Open the captured image file
        with open(local_file_path, 'rb') as f:
            files = {'file': f}
            token = TokenManager.load_token()
            headers = {'Authorization': f'Bearer {token}'}

            # Upload the image to Django API, which will handle Cloudinary upload
            response = requests.post(ENDPOINTS['upload_icon'], files=files, headers=headers)

        if response.status_code == 201:
            # Extract the secure URL returned by the Django API
            icon_url = response.json().get('secure_url')

            # Save the icon with the correct name locally
            correct_local_path = os.path.join(save_dir, os.path.basename(icon_url))
            os.rename(local_file_path, correct_local_path)

            # Post the category to the database using the Cloudinary URL
            self.post_category_to_db(icon_url)
        else:
            self.show_popup('Error', 'Failed to upload icon to the server.')

    def post_category_to_db(self, icon_url):
        """Send a POST request to the backend to create the category."""
        url = ENDPOINTS['categories']
        token = TokenManager.load_token()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'name': self.category_name,
            'type': self.selected_type,
            'icon': icon_url,  # This is the full URL returned by Cloudinary
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            self.show_popup('Success', 'Category created successfully.')
        else:
            self.show_popup('Error', 'Failed to create category.')

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.25))
        box.add_widget(btn)
        popup = Popup(title=title, content=box, size_hint=(0.8, 0.5))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def toggle_display(self, display_type):
        if display_type == 'icon':
            self.ids.icon_grid.height = self.ids.icon_grid.minimum_height
            self.ids.icon_grid.opacity = 1
            self.ids.icon_grid.disabled = False

            self.ids.color_grid.height = 0
            self.ids.color_grid.opacity = 0
            self.ids.color_grid.disabled = True

        elif display_type == 'color':
            self.ids.icon_grid.height = 0
            self.ids.icon_grid.opacity = 0
            self.ids.icon_grid.disabled = True

            self.ids.color_grid.height = self.ids.color_grid.minimum_height
            self.ids.color_grid.opacity = 1
            self.ids.color_grid.disabled = False

    def on_icon_button_press(self, instance):
        self.toggle_display('icon')
        self.ids.icon_button.background_normal = 'kivy_app/assets/img/Rectangle_down.png'
        self.ids.color_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'

    def on_color_button_press(self, instance):
        self.toggle_display('color')
        self.ids.icon_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'
        self.ids.color_button.background_normal = 'kivy_app/assets/img/Rectangle_down.png'
