from kivy.uix.screenmanager import Screen


class TransactionScreen(Screen):

    def go_back(self, instance):
        self.manager.current = 'home'
