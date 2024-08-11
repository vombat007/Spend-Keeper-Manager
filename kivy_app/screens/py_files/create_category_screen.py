import os
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle


class CreateCategoryScreen(Screen):
    selected_icon = StringProperty('')
    selected_color = ListProperty([1, 1, 1, 1])
    category_name = StringProperty('')

    def on_pre_enter(self, *args):
        self.display_icons()
        self.toggle_display('icon')  # Default to showing icons

    def display_icons(self):
        icon_grid = self.ids.icon_grid
        icon_grid.clear_widgets()
        icon_path = 'kivy_app/assets/icon/all/'

        for icon_file in os.listdir(icon_path):
            if icon_file.endswith('.png'):
                btn = Button(
                    size_hint=(None, None),
                    size=(64, 64),
                    background_normal=os.path.join(icon_path, icon_file),
                    background_down=os.path.join(icon_path, icon_file)
                )
                btn.bind(on_press=self.select_icon)
                btn.icon_path = os.path.join(icon_path, icon_file)
                icon_grid.add_widget(btn)

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

    def select_color(self, instance, color):
        self.selected_color = color
        self.update_selected_icon()

    def create_category(self):
        if not self.category_name or not self.selected_icon:
            self.show_popup('Error', 'Please provide all the details.')
            return

        # Implement the logic to create and save the new category
        self.show_popup('Success', f'Category {self.category_name} created successfully!')

    def show_popup(self, title, message):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, 0.25))
        box.add_widget(btn)
        popup = Popup(title=title, content=box, size_hint=(0.8, 0.5))
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def toggle_display(self, display_type):
        """Toggle between icon grid and color picker display."""
        if display_type == 'icon':
            self.ids.icon_grid.height = dp(200)
            self.ids.icon_grid.opacity = 1
            self.ids.icon_grid.disabled = False

            self.ids.color_picker.height = 0
            self.ids.color_picker.opacity = 0
            self.ids.color_picker.disabled = True

        elif display_type == 'color':
            self.ids.icon_grid.height = 0
            self.ids.icon_grid.opacity = 0
            self.ids.icon_grid.disabled = True

            self.ids.color_picker.height = dp(200)
            self.ids.color_picker.opacity = 1
            self.ids.color_picker.disabled = False

    def on_icon_button_press(self, instance):
        self.toggle_display('icon')
        self.ids.icon_button.background_normal = 'kivy_app/assets/img/Rectangle_down.png'
        self.ids.color_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'

    def on_color_button_press(self, instance):
        self.toggle_display('color')
        self.ids.icon_button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'
        self.ids.color_button.background_normal = 'kivy_app/assets/img/Rectangle_down.png'
