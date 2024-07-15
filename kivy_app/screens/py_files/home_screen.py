import json
import os
import requests
from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from datetime import datetime, timedelta
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from widget.date_picker_app import DatePicker


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
    current_date = datetime.now()
    start_date = None
    end_date = None
    income_label = ObjectProperty(None)
    expense_label = ObjectProperty(None)
    period_label = ObjectProperty(None)
    accounts = []
    current_account_index = 0

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = self.load_token()
        self.selected_button = None
        self.fetch_accounts()

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
        self.update_button_visibility()

    def refresh_token_if_needed(self):
        response = requests.post('http://127.0.0.1:8000/api/login/verify/', data={
            'token': self.token
        })
        if response.status_code != 200:
            app = App.get_running_app()
            self.token = app.refresh_token()
        return self.token

    def fetch_accounts(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get('http://127.0.0.1:8000/api/accounts/', headers=headers)
        if response.status_code == 200:
            self.accounts = response.json()
            self.current_account_index = 0  # Start with the first account
            self.fetch_account_summary()
        else:
            print("Failed to fetch accounts")

    def fetch_account_summary(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        current_account_id = self.accounts[self.current_account_index]['id']

        if self.selected_period == 'period':
            if not self.start_date or not self.end_date:
                print("Please select a date range.")
                return
            url = f'http://127.0.0.1:8000/api/account/{current_account_id}/summary/?start_date={self.start_date}&end_date={self.end_date}'
        elif self.selected_period in ['day', 'week', 'month', 'year']:
            start_date, end_date = self.get_period_dates()
            url = f'http://127.0.0.1:8000/api/account/{current_account_id}/summary/?start_date={start_date}&end_date={end_date}'

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.chart.update_chart(data['total_balance'], data['percent_spent'], data['account_name'])
            self.update_income_expense(data['income'], data['expense'])
        else:
            print("Failed to fetch account summary")

    def get_period_dates(self):
        if self.selected_period == 'day':
            start_date = self.current_date.strftime('%Y-%m-%d')
            end_date = start_date
        elif self.selected_period == 'week':
            start_date = (self.current_date - timedelta(days=self.current_date.weekday())).strftime('%Y-%m-%d')
            end_date = (self.current_date + timedelta(days=6 - self.current_date.weekday())).strftime('%Y-%m-%d')
        elif self.selected_period == 'month':
            start_date = self.current_date.replace(day=1).strftime('%Y-%m-%d')
            next_month = self.current_date.replace(day=28) + timedelta(days=4)  # this will never fail
            end_date = (next_month - timedelta(days=next_month.day)).strftime('%Y-%m-%d')
        elif self.selected_period == 'year':
            start_date = self.current_date.replace(month=1, day=1).strftime('%Y-%m-%d')
            end_date = self.current_date.replace(month=12, day=31).strftime('%Y-%m-%d')
        return start_date, end_date

    def update_income_expense(self, income, expense):
        self.income_label.text = f'Income \n  ${income}'
        self.expense_label.text = f'Expense \n   ${expense}'

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
        self.current_date = datetime.now()  # Reset to today whenever period changes
        self.update_period_label()
        if period == 'period':
            date_picker = DatePicker()  # Use custom DatePicker
            date_picker.on_done = self.on_date_picker_done
            date_picker.on_cancel = self.on_date_picker_cancel
            center_x = (Window.width - date_picker.width) / 2
            center_y = (Window.height - date_picker.height) / 2
            date_picker.pos = (center_x, center_y)
            self.add_widget(date_picker)
        else:
            self.fetch_account_summary()

    def on_date_picker_done(self, instance):
        if instance.start_date:
            self.start_date = instance.start_date.strftime('%Y-%m-%d')
            self.end_date = instance.end_date.strftime('%Y-%m-%d') if instance.end_date else self.start_date
            self.fetch_account_summary()
        instance.animate_close()
        self.reset_period_button_state()

        # Set the period button state to background_down
        period_button = self.ids.period_button
        period_button.background_normal = period_button.background_down

    def on_date_picker_cancel(self, instance):
        instance.animate_close()
        self.reset_period_button_state()

        # Reset to the default month button
        self.set_period('month')
        self.ids.month_button.state = 'down'

    def reset_period_button_state(self):
        # Reset the state of all period buttons
        button_ids = ['day_button', 'week_button', 'month_button', 'year_button', 'period_button']
        for button_id in button_ids:
            button = self.ids.get(button_id)
            if button:
                button.state = 'normal'
                button.background_normal = 'kivy_app/assets/img/Rectangle_normal.png'

    def set_default_selected_button(self):
        if not self.selected_button:
            self.selected_button = self.ids.month_button
            self.selected_button.state = 'down'
            self.set_period('month')

    def update_period_label(self):
        if self.selected_period == 'day':
            today = datetime.now().date()
            selected_day = self.current_date.date()
            days_ago = (today - selected_day).days

            if days_ago == 0:
                self.period_label.text = f'Today, {selected_day.strftime("%B %d")}'
            elif days_ago == 1:
                self.period_label.text = f'Yesterday, {selected_day.strftime("%B %d")}'
            else:
                self.period_label.text = selected_day.strftime('%B %d')
        elif self.selected_period == 'week':
            start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            self.period_label.text = f'{start_of_week.strftime("%b %d")} - {end_of_week.strftime("%b %d")}'
        elif self.selected_period == 'month':
            self.period_label.text = self.current_date.strftime('%B %Y')
        elif self.selected_period == 'year':
            self.period_label.text = self.current_date.strftime('%Y')

    def change_period(self, direction):
        new_date = self.current_date
        if self.selected_period == 'day':
            new_date += timedelta(days=direction)
        elif self.selected_period == 'week':
            new_date += timedelta(weeks=direction)
        elif self.selected_period == 'month':
            month = new_date.month - 1 + direction
            year = new_date.year + month // 12
            month = month % 12 + 1
            day = min(new_date.day,
                      [31, 29 if year % 4 == 0 and not year % 100 == 0 or year % 400 == 0 else 28, 31, 30,
                       31, 30, 31, 31, 30, 31, 30, 31][month - 1])
            new_date = new_date.replace(year=year, month=month, day=day)
        elif self.selected_period == 'year':
            new_date = new_date.replace(year=new_date.year + direction)

        # Ensure the new date is not in the future
        if new_date <= datetime.now():
            self.current_date = new_date
            self.update_period_label()
            self.fetch_account_summary()
        else:
            print("Cannot set a period in the future.")

        # Update the visibility of the buttons
        self.update_button_visibility()

    def switch_account(self, direction):
        self.current_account_index = (self.current_account_index + direction) % len(self.accounts)
        self.fetch_account_summary()

    # Ensure the new methods are called when the arrow buttons are pressed
    def update_button_visibility(self):
        now = datetime.now()

        left_button = self.ids.left_arrow_button
        right_button = self.ids.right_arrow_button

        left_button.disabled = len(self.accounts) <= 1
        right_button.disabled = len(self.accounts) <= 1

        if self.selected_period == 'day':
            left_button.disabled = False
            right_button.disabled = self.current_date >= now
        elif self.selected_period == 'week':
            left_button.disabled = False
            right_button.disabled = self.current_date + timedelta(weeks=1) > now
        elif self.selected_period == 'month':
            next_month = self.current_date.replace(day=28) + timedelta(days=4)  # this will never fail
            end_of_month = next_month - timedelta(days=next_month.day)
            left_button.disabled = False
            right_button.disabled = end_of_month >= now
        elif self.selected_period == 'year':
            left_button.disabled = False
            right_button.disabled = self.current_date.replace(year=self.current_date.year + 1) > now
