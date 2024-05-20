from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.finance_screen import FinanceScreen
from kivy_app.screens.login_screen import LoginScreen
from kivy_app.screens.registration_screen import RegistrationScreen


class FinancialApp(App):
    def build(self):
        self.title = 'Financial App'

        sm = ScreenManager()

        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FinanceScreen(name='finance'))

        return sm


if __name__ == '__main__':
    FinancialApp().run()
