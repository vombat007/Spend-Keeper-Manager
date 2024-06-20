import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy_app.screens.py_files.home_screen import HomeScreen
from kivy_app.screens.py_files.finance_screen import FinanceScreen
from kivy_app.screens.py_files.login_screen import LoginScreen
from kivy_app.screens.py_files.registration_screen import RegistrationScreen
from kivy_app.screens.py_files.splash_screen import SplashScreen
from kivy_app.screens.py_files.start_screen import StartScreen
from kivy_app.screens.py_files.sidebar_menu import SidebarMenu


class FinancialApp(App):
    def build(self):
        self.title = 'Financial App'

        # Load the KV files
        Builder.load_file('kivy_app/screens/kv_files/start_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/login_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/registration_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/home_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/sidebar_menu.kv')

        sm = ScreenManager()

        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(HomeScreen(screen_manager=sm, name='home'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FinanceScreen(name='finance'))

        if self.is_user_logged_in():
            sm.current = 'home'
        else:
            sm.current = 'start'

        return sm

    @staticmethod
    def is_user_logged_in():
        return os.path.exists('token.txt')


if __name__ == '__main__':
    FinancialApp().run()
