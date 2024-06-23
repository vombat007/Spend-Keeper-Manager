from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation


class CustomSidebarButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_sidebar_open = False
        self.update_style()

    def toggle(self):
        self.is_sidebar_open = not self.is_sidebar_open
        self.update_style()

    def update_style(self):
        if self.is_sidebar_open:
            self.background_normal = 'kivy_app/assets/img/return_button.png'
        else:
            self.background_normal = 'kivy_app/assets/img/settings_button.png'


class HomeScreen(Screen):
    sidebar = ObjectProperty(None)

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = None

    def set_token(self, token):
        self.token = token
        with open('token.txt', 'w') as token_file:
            token_file.write(token)

    def toggle_sidebar(self):
        button = self.ids.sidebar_toggle_button
        button.toggle()

        if self.sidebar.x < 0:
            anim = Animation(x=0, duration=0.3)
        else:
            anim = Animation(x=-self.sidebar.width, duration=0.3)
        anim.start(self.sidebar)
