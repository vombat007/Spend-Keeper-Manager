from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import NumericProperty
from kivy.uix.label import Label


class CircularChart(Widget):
    total_balance = NumericProperty(0)
    percent_spent = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spent_label = Label(text="", color=(0.5, 0, 0, 1), font_size='20sp', bold=True)
        self.add_widget(self.spent_label)
        self.bind(size=self.update_chart, pos=self.update_chart)
        self.update_chart()

    def update_chart(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Draw the background circle
            Color(0.8, 0.8, 0.8, 1)  # Light gray for the remaining portion
            Ellipse(pos=self.pos, size=self.size, angle_start=0, angle_end=360)

            # Draw the spent portion
            Color(1, 1, 0, 1)  # Yellow for the spent portion
            Ellipse(pos=self.pos, size=self.size, angle_start=0, angle_end=(self.percent_spent / 100) * 360)

            # Draw the inner circle to create a ring effect
            Color(1, 1, 1, 1)  # White inner circle
            inner_size = (self.size[0] * 0.8, self.size[1] * 0.8)  # Adjust size for the ring effect
            inner_pos = (self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.1)
            Ellipse(pos=inner_pos, size=inner_size)

            # Draw the black outlines
            Color(0, 0, 0, 1)  # Black color for outlines
            outer_radius = self.size[0] / 2
            inner_radius = self.size[0] * 0.4
            Line(circle=(self.center_x, self.center_y, outer_radius), width=3)  # Outer outline
            Line(circle=(self.center_x, self.center_y, inner_radius), width=2)  # Inner outline

        self.spent_label.text = f"{self.percent_spent}%\nspent"

    def on_size(self, *args):
        self.update_chart()

    def on_pos(self, *args):
        self.update_chart()
