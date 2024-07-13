from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import datetime, timedelta


class DatePicker(FloatLayout):
    current_date = StringProperty()
    on_done = None  # Callback for done action
    on_cancel = None  # Callback for cancel action

    def __init__(self, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.selected_date = datetime.now()
        self.start_date = None
        self.end_date = None

        self.update_header()
        self.update_body()

        # Initialize the "Done" button state
        self.ids.done_button.disabled = True

    def update_header(self):
        self.ids.header.clear_widgets()
        prev_button = self.ids.prev_button
        prev_button.bind(on_press=self.prev_month)
        self.ids.header.add_widget(prev_button)

        self.month_year_label = self.ids.month_year_label
        self.month_year_label.text = self.selected_date.strftime('%B %Y')
        self.ids.header.add_widget(self.month_year_label)

        next_button = self.ids.next_button
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
                day_button = self.create_day_button(str(i), 'kivy_app/assets/img/Yellow_circle.png')

            elif date == self.start_date or date == self.end_date:
                day_button = self.create_day_button(str(i), 'kivy_app/assets/img/Yellow_circle.png')

            elif date.day == current_day and date.month == datetime.now().month and date.year == datetime.now().year:
                day_button = self.create_day_button(str(i), 'kivy_app/assets/img/Red_circle.png')

            elif date < datetime.now():
                day_button = self.create_day_button(str(i), '', (0.7, 0.7, 0.7, 1))
            else:
                day_button = self.create_day_button(str(i))

            day_button.bind(on_press=self.select_date)
            self.ids.body.add_widget(day_button)

    def create_day_button(self, text, background_normal='', color=(0, 0, 0, 1)):
        return Button(text=text, size_hint=(None, None), size=(40, 40),
                      background_normal=background_normal,
                      background_down='',
                      color=color)

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

        # Enable the "Done" button
        self.ids.done_button.disabled = False

    def cancel(self, instance):
        if self.on_cancel:
            self.on_cancel(self)
        self.animate_close()

    def done(self, instance):
        if self.start_date and not self.end_date:
            self.end_date = self.start_date  # Set end_date to start_date if not set
        if self.on_done:
            self.on_done(self)
        self.animate_close()

    def animate_close(self):
        anim = Animation(opacity=0, y=self.y - 100, duration=0.3)

        def remove_widget_from_parent(*args):
            if self.parent:
                self.parent.remove_widget(self)

        anim.bind(on_complete=remove_widget_from_parent)
        anim.start(self)
