import os
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy_app.config import WINDOWS_SIZE
from kivy_app.screens.py_files.home_screen import HomeScreen
from kivy_app.screens.py_files.sidebar_menu import SidebarMenu
from kivy_app.screens.py_files.start_screen import StartScreen
from kivy_app.screens.py_files.login_screen import LoginScreen
from kivy_app.screens.py_files.splash_screen import SplashScreen
from kivy_app.screens.py_files.transaction_screen import TransactionScreen
from kivy_app.screens.py_files.registration_screen import RegistrationScreen
from kivy_app.screens.py_files.calculator_screen import CalculatorScreen
from kivy_app.screens.py_files.create_category_screen import CreateCategoryScreen
from kivy_app.utils import TokenManager, download_all_icons_from_cloudinary


class FinancialApp(App):
    token = None

    def build(self):
        self.title = 'Financial App'

        # Simulate the viewport size for development
        Window.size = WINDOWS_SIZE

        # Load the KV files
        Builder.load_file('kivy_app/widget/date_picker_app.kv')
        Builder.load_file('kivy_app/screens/kv_files/start_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/login_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/registration_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/home_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/sidebar_menu.kv')
        Builder.load_file('kivy_app/screens/kv_files/transaction_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/calculator_screen.kv')
        Builder.load_file('kivy_app/screens/kv_files/create_category_screen.kv')

        # Ensure all icons are available locally before loading screens
        self.ensure_local_icons()

        self.token = TokenManager.load_token()

        sm = ScreenManager()

        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(screen_manager=sm, name='home'))
        sm.add_widget(TransactionScreen(name='transaction'))
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(CreateCategoryScreen(name='create_category'))

        if self.is_user_logged_in():
            sm.current = 'home'
        else:
            sm.current = 'start'

        # Bind the back button event
        Window.bind(on_keyboard=self.on_back_button)

        self.sm = sm
        return sm

    @staticmethod
    def ensure_local_icons():
        # Download all icons from cloudinary to local storage
        download_all_icons_from_cloudinary('kivy_app/assets/icon/all/')

    @staticmethod
    def is_user_logged_in():
        return os.path.exists('tokens.json')

    def on_back_button(self, window, key, *args):
        if key == 27:  # 27 is the code for the back button
            if self.sm.current == 'transaction':
                self.sm.current = 'home'  # Go to the home screen if on transaction screen
            elif self.sm.current == 'home':
                self.stop()  # Close the app if on the home screen
            else:
                self.sm.current = 'home'  # Go to the home screen otherwise
            return True
        return False


if __name__ == '__main__':
    FinancialApp().run()
