from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
import requests
import json
import os


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
    chart = ObjectProperty(None)
    selected_period = 'year'  # Default period

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = self.load_token()

    @staticmethod
    def load_token():
        if os.path.exists('tokens.json'):
            with open('tokens.json', 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('access')
        return None

    def on_pre_enter(self):
        self.token = self.refresh_token_if_needed()
        self.fetch_account_summary()

    def refresh_token_if_needed(self):
        response = requests.post('http://127.0.0.1:8000/api/login/verify/', data={
            'token': self.token
        })
        if response.status_code != 200:
            app = App.get_running_app()
            self.token = app.refresh_token()
        return self.token

    def fetch_account_summary(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f'http://127.0.0.1:8000/api/account/1/summary/?period={self.selected_period}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.chart.update_chart(data['total_balance'], data['percent_spent'], data['account_name'])
        else:
            print("Failed to fetch account summary")

    def toggle_sidebar(self):
        button = self.ids.sidebar_toggle_button
        button.toggle()

        if self.sidebar.x < 0:
            anim = Animation(x=0, duration=0.3)
        else:
            anim = Animation(x=-self.sidebar.width, duration=0.3)
        anim.start(self.sidebar)

    def go_finance(self, instance):
        self.manager.current = 'finance'

    def set_period(self, period):
        self.selected_period = period
        self.fetch_account_summary()
