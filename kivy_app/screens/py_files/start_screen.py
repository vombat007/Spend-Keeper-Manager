from kivy.uix.screenmanager import Screen


class StartScreen(Screen):
    def sign_up(self, instance):
        self.manager.current = 'registration'
