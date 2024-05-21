from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy_app.screens.home_screen import HomeScreen
from kivy_app.screens.finance_screen import FinanceScreen
from kivy_app.screens.login_screen import LoginScreen
from kivy_app.screens.registration_screen import RegistrationScreen
from kivy_app.screens.splash_screen import SplashScreen


class FinancialApp(App):
    def build(self):
        self.title = 'Financial App'

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


