from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from datetime import datetime, timedelta

Builder.load_file('date_picker_app.kv')


class DatePicker(FloatLayout):
    current_date = StringProperty()

    def __init__(self, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.selected_date = datetime.now()
        self.start_date = None
        self.end_date = None

        self.update_header()
        self.update_body()
        self.update_footer()

    def update_header(self):
        self.ids.header.clear_widgets()

        prev_button = Button(size_hint=(None, None), size=(45, 32),
                             background_normal='Button_arrow_left_normal.png',
                             background_down='Button_arrow_left_down.png'
                             )
        prev_button.bind(on_press=self.prev_month)
        self.ids.header.add_widget(prev_button)

        self.month_year_label = Label(text=self.selected_date.strftime('%B %Y'),
                                      size_hint=(None, None),
                                      size=(200, 40),
                                      color=(0, 0, 0, 1))
        self.ids.header.add_widget(self.month_year_label)

        next_button = Button(size_hint=(None, None), size=(45, 32),
                             background_normal='Button_arrow_right_normal.png',
                             background_down='Button_arrow_right_down.png'
                             )
        next_button.bind(on_press=self.next_month)
        self.ids.header.add_widget(next_button)

    def update_body(self):
        self.ids.body.clear_widgets()

        days = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        for i, day in enumerate(days):
            color = (1, 0, 0, 1) if i == 0 else (0, 0, 0, 1)  # Red for Sunday
            self.ids.body.add_widget(Label(text=day, size_hint=(None, None), size=(40, 40), color=color))

        first_day = self.selected_date.replace(day=1)
        start_day = first_day.weekday()
        if start_day == 6:  # Adjusting for Sunday start
            start_day = -1

        days_in_month = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        current_day = datetime.now().day
        for _ in range(start_day + 1):
            self.ids.body.add_widget(Label(text='', size_hint=(None, None), size=(40, 40)))

        for i in range(1, days_in_month + 1):
            date = self.selected_date.replace(day=i)
            if self.start_date and self.end_date and self.start_date <= date <= self.end_date:
                day_button = Button(text=str(i), size_hint=(None, None), size=(40, 40), background_normal='',
                                    background_down='', background_color=(1, 1, 0, 1), color=(0, 0, 0, 1))
            elif date == self.start_date or date == self.end_date:
                day_button = Button(text=str(i), size_hint=(None, None), size=(40, 40), background_normal='',
                                    background_down='', background_color=(1, 1, 0, 1), color=(0, 0, 0, 1))
            elif date.day == current_day and date.month == datetime.now().month and date.year == datetime.now().year:
                day_button = Button(text=str(i), size_hint=(None, None), size=(40, 40), background_normal='',
                                    background_down='', background_color=(1, 0, 0, 1), color=(0, 0, 0, 1))  # Highlight current day
            elif date < datetime.now():
                day_button = Button(text=str(i), size_hint=(None, None), size=(40, 40), background_normal='',
                                    background_down='', color=(0.7, 0.7, 0.7, 1))  # Pale color for past days
            else:
                day_button = Button(text=str(i), size_hint=(None, None), size=(40, 40), background_normal='',
                                    background_down='', background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
            day_button.bind(on_press=self.select_date)
            self.ids.body.add_widget(day_button)

    def update_footer(self):
        self.ids.footer.clear_widgets()

        cancel_button = Button(text='Cancel', font_size=20, size_hint=(None, None), size=(120, 40),
                               background_normal='', background_down='', background_color=(0.7, 0.7, 0.7, 1),
                               color=(0, 0, 0, 1))
        cancel_button.bind(on_press=self.cancel)
        self.ids.footer.add_widget(cancel_button)

        done_button = Button(text='Done', font_size=20, size_hint=(None, None), size=(120, 40), background_normal='',
                             background_down='', background_color=(1, 1, 0, 1), color=(0, 0, 0, 1))
        done_button.bind(on_press=self.done)
        self.ids.footer.add_widget(done_button)

    def prev_month(self, instance):
        Clock.schedule_once(self._prev_month_callback, 0.1)

    def _prev_month_callback(self, dt):
        first_day = self.selected_date.replace(day=1)
        prev_month = first_day - timedelta(days=1)
        self.selected_date = prev_month.replace(day=1)
        self.update_header()
        self.update_body()

    def next_month(self, instance):
        Clock.schedule_once(self._next_month_callback, 0.1)

    def _next_month_callback(self, dt):
        first_day = self.selected_date.replace(day=1)
        next_month = first_day + timedelta(days=31)
        self.selected_date = next_month.replace(day=1)
        self.update_header()
        self.update_body()

    def select_date(self, instance):
        day = int(instance.text)
        selected_date = self.selected_date.replace(day=day)

        if self.start_date is None or (self.start_date and self.end_date):
            self.start_date = selected_date
            self.end_date = None
        elif self.start_date and not self.end_date:
            if selected_date < self.start_date:
                self.start_date = selected_date
            else:
                self.end_date = selected_date

        self.update_body()

    def cancel(self, instance):
        # Logic to cancel the date selection
        print("Date selection cancelled.")
        self.start_date = None
        self.end_date = None
        self.update_body()

    def done(self, instance):
        if self.start_date and self.end_date:
            print(f"Start date: {self.start_date.strftime('%Y-%m-%d')}, End date: {self.end_date.strftime('%Y-%m-%d')}")
        elif self.start_date:
            print(f"Start date: {self.start_date.strftime('%Y-%m-%d')}")
        else:
            print("No date selected.")
        # Logic to confirm the date selection
        # Reset selection after confirming
        self.start_date = None
        self.end_date = None
        self.update_body()


class DatePickerApp(App):
    def build(self):
        root = FloatLayout()
        date_picker = DatePicker(size_hint=(None, None), size=(350, 400), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        root.add_widget(date_picker)
        return root


if __name__ == '__main__':
    DatePickerApp().run()
