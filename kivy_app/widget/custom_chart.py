from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.core.text import Label as CoreLabel
from kivy.lang import Builder

Builder.load_string('''
<CircularChart>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Ellipse:
            pos: self.pos
            size: self.size
            angle_start: 0
            angle_end: 360
        Color:
            rgba: 1, 1, 0, 1  # Yellow for remaining
        Line:
            circle: (self.center_x, self.center_y, self.radius, 0, self.spent_angle)
            width: self.line_width
        Color:
            rgba: 0.5, 0.5, 0.5, 1  # Grey for spent
        Line:
            circle: (self.center_x, self.center_y, self.radius, self.spent_angle, 360)
            width: self.line_width
''')

class CircularChart(Widget):
    total_balance = NumericProperty(0)
    percent_spent = NumericProperty(0)
    account_name = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas, pos=self.update_canvas)

    @property
    def spent_angle(self):
        return 360 * (self.percent_spent / 100)

    @property
    def radius(self):
        return min(self.size) / 2

    @property
    def line_width(self):
        return self.radius / 8

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Ellipse(pos=self.pos, size=self.size, angle_start=0, angle_end=360)
            Color(1, 1, 0, 1)
            Line(circle=(self.center_x, self.center_y, self.radius, 0, self.spent_angle), width=self.line_width)
            Color(0.5, 0.5, 0.5, 1)
            Line(circle=(self.center_x, self.center_y, self.radius, self.spent_angle, 360), width=self.line_width)

            # Draw inner black stroke
            Color(0, 0, 0, 1)
            Line(circle=(self.center_x, self.center_y, self.radius - self.line_width / 1, 0, 360), width=2)

            # Draw outer black stroke
            Color(0, 0, 0, 1)
            Line(circle=(self.center_x, self.center_y, self.radius + self.line_width / 1, 0, 360), width=3)

            # Draw the account name in the center
            self.draw_text(self.account_name, self.center_x, self.center_y + 60)
            # Draw the total balance in the center
            self.draw_text(f'Balance $: {self.total_balance}', self.center_x, self.center_y - 10)

            self.draw_text(f'Spend %: {self.percent_spent}', self.center_x, self.center_y - 50)

    def draw_text(self, text, x, y):
        label = CoreLabel(text=text, font_size=20, color=(0, 0, 0, 1))
        label.refresh()
        text_texture = label.texture
        text_pos = (x - text_texture.width / 2, y - text_texture.height / 2)
        Color(0, 0, 0, 1)
        Rectangle(texture=text_texture, pos=text_pos, size=text_texture.size)

    def update_chart(self, total_balance, percent_spent, account_name):
        self.total_balance = total_balance
        self.percent_spent = percent_spent
        self.account_name = account_name
        self.update_canvas()
