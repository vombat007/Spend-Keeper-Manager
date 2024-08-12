import os
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle


class CreateCategoryScreen(Screen):
    selected_icon = StringProperty('')
    selected_color = ListProperty([1, 1, 1, 1])
    category_name = StringProperty('')

    def on_pre_enter(self, *args):
        self.display_icons()
        self.display_color_options()
        self.toggle_display('icon')  # Default to showing icons

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
            [0.753, 0.047, 0.047, 1.0],
            [0.753, 0.059, 0.047, 1.0],
            [0.925, 0.133, 0.122, 1.0],
            [0.871, 0.29, 0.29, 1.0],
            [0.831, 0.176, 0.176, 1.0],
            [0.965, 0.231, 0.231, 1.0],
            [0.949, 0.392, 0.392, 1.0],
            [1.0, 0.0, 0.0, 1.0],
            [0.894, 0.098, 0.098, 1.0],
            [1.0, 0.216, 0.216, 1.0],
            [1.0, 0.251, 0.251, 1.0],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 0.5, 0, 1],
            [0.5, 0, 0.5, 1],
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [0.5, 0.5, 0.5, 1],
            [0, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 0.5, 0, 1],
            [0.5, 0, 0.5, 1],
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [0.5, 0.5, 0.5, 1],
            [0, 0, 0, 1],
            [0, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 0.5, 0, 1],
            [0.5, 0, 0.5, 1],
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [0.5, 0.5, 0.5, 1],
            [0, 0, 0, 1],
        ]

        for color in color_choices:
            btn = Button(
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                background_normal='',
                background_down='',
                background_color=color
            )
            btn.bind(on_press=lambda instance, color=color: self.select_color(instance, color))
            color_grid.add_widget(btn)

    def select_color(self, instance, color):
        self.selected_color = color
        self.update_selected_icon()

    def create_category(self):
        if not self.category_name or not self.selected_icon:
            self.show_popup('Error', 'Please provide all the details.')
            return

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
        if display_type == 'icon':
            self.ids.icon_grid.height = self.ids.icon_grid.minimum_height
            self.ids.icon_grid.size_hint_y = None
            self.ids.icon_grid.opacity = 1
            self.ids.icon_grid.disabled = False

            self.ids.color_grid.height = 0
            self.ids.color_grid.size_hint_y = None
            self.ids.color_grid.opacity = 0
            self.ids.color_grid.disabled = True

        elif display_type == 'color':
            self.ids.icon_grid.height = 0
            self.ids.icon_grid.size_hint_y = None
            self.ids.icon_grid.opacity = 0
            self.ids.icon_grid.disabled = True

            self.ids.color_grid.height = dp(200)
            self.ids.color_grid.size_hint_y = None
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
