from kivy.uix.screenmanager import Screen


class StartScreen(Screen):
    def sing_up(self, instance):
        self.manager.current = 'registration'
