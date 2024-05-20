from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout


class SidebarMenu(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = 200
        self.height = 50  # Initial height of the menu button

        self.menu_button = ToggleButton(text='☰', size_hint=(None, None), size=(self.width, 50))
        self.menu_button.bind(on_release=self.toggle_menu)
        self.add_widget(self.menu_button)

        self.menu_layout = GridLayout(cols=1, size_hint_y=None, height=0)

        self.login_button = Button(text='Login')
        self.login_button.bind(on_release=self.go_to_login)
        self.menu_layout.add_widget(self.login_button)

        self.registration_button = Button(text='Registration')
        self.registration_button.bind(on_release=self.go_to_registration)
        self.menu_layout.add_widget(self.registration_button)

        self.settings_button = Button(text='Settings')
        self.settings_button.bind(on_release=self.go_to_settings)
        self.menu_layout.add_widget(self.settings_button)

        self.add_widget(self.menu_layout)

    def toggle_menu(self, instance):
        if self.menu_button.state == 'down':
            self.menu_layout.height = len(self.menu_layout.children) * 50
            self.height = 50 + self.menu_layout.height
        else:
            self.menu_layout.height = 0
            self.height = 50

    def go_to_login(self, instance):
        self.screen_manager.current = 'login'

    def go_to_registration(self, instance):
        self.screen_manager.current = 'registration'

    def go_to_settings(self, instance):
        self.screen_manager.current = 'settings'
