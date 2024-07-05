from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.pickers import MDDockedDatePicker
import requests
import json
import os
from datetime import datetime


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


class CustomButton(Button):
    all_buttons = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_button()

    def register_button(self):
        CustomButton.all_buttons.append(self)

    def on_release(self):
        if self.state == 'down':
            self.background_normal = 'kivy_app/assets/img/Rectangle_down.png'
            self.color = (0, 0, 0, 1)
            self.deselect_other_buttons()
        else:
            self.state = 'down'

    def deselect_other_buttons(self):
        for button in CustomButton.all_buttons:
            if button != self:
                button.state = 'normal'
                button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'


class HomeScreen(Screen):
    sidebar = ObjectProperty(None)
    chart = ObjectProperty(None)
    selected_period = 'month'  # Default period
    start_date = None
    end_date = None

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = self.load_token()
        self.selected_button = None

    @staticmethod
    def load_token():
        if os.path.exists('tokens.json'):
            with open('tokens.json', 'r') as token_file:
                tokens = json.load(token_file)
                return tokens.get('access')
        return None

    def on_pre_enter(self):
        self.token = self.refresh_token_if_needed()
        self.set_default_selected_button()

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
        if self.selected_period == 'period':
            if not self.start_date or not self.end_date:
                print("Please select a date range.")
                return
            url = f'http://127.0.0.1:8000/api/account/1/summary/?start_date={self.start_date}&end_date={self.end_date}'
        else:
            url = f'http://127.0.0.1:8000/api/account/1/summary/?period={self.selected_period}'

        response = requests.get(url, headers=headers)
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
        if period == 'period':
            date_picker = MDDockedDatePicker(mode='range')
            date_picker.bind(on_ok=self.on_ok, on_cancel=self.on_cancel)
            date_picker.open()
        else:
            self.fetch_account_summary()

    def on_ok(self, instance):
        date_range = instance
        print(instance.get_date()[0].strftime('%Y-%m-%d'))
        print(instance.get_date()[-1].strftime('%Y-%m-%d'))
        self.start_date = instance.get_date()[0].strftime('%Y-%m-%d')
        self.end_date = instance.get_date()[-1].strftime('%Y-%m-%d')
        self.fetch_account_summary()

    def on_cancel(self, instance, value):
        pass

    def set_default_selected_button(self):
        if not self.selected_button:
            self.selected_button = self.ids.month_button
            self.selected_button.state = 'down'
            self.set_period('month')
