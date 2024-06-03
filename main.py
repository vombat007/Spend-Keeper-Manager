from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy_app.screens.py_files.home_screen import HomeScreen
from kivy_app.screens.py_files.finance_screen import FinanceScreen
from kivy_app.screens.py_files.login_screen import LoginScreen
from kivy_app.screens.py_files.registration_screen import RegistrationScreen
from kivy_app.screens.py_files.splash_screen import SplashScreen
from kivy.lang import Builder


class FinancialApp(App):
    def build(self):
        self.title = 'Financial App'

        Builder.load_file('kivy_app/screens/kv_files/login_screen.kv')
        # Builder.load_file('kivy_app/screens/kv_files/home_screen.kv')

        sm = ScreenManager()

        # Add splash screen first
        sm.add_widget(SplashScreen(name='splash', frame_rate=11))  # Adjust frame rate if needed

        # Add other screens
        sm.add_widget(HomeScreen(screen_manager=sm, name='home'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(FinanceScreen(name='finance'))

        # Set splash screen as the initial screen
        sm.current = 'splash'

        return sm


if __name__ == '__main__':
    FinancialApp().run()


