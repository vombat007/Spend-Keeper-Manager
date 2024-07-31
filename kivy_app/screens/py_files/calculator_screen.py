from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class CalculatorScreen(Screen):
    display_text = StringProperty("0")

    def go_back(self, instance):
        self.manager.current = 'transaction'

    def clear(self):
        self.display_text = "0"

    def half(self):
        if self.display_text:
            self.display_text = str(float(self.display_text) / 2)

    def percent(self):
        if self.display_text:
            self.display_text = str(float(self.display_text) / 100)

    def add_number(self, number):
        if self.display_text == "0":
            self.display_text = str(number)
        else:
            self.display_text += str(number)

    def add_operator(self, operator):
        if self.display_text[-1] not in "+-*/":
            self.display_text += operator

    def add_dot(self):
        if "." not in self.display_text:
            self.display_text += "."

    def calculate(self):
        try:
            self.display_text = str(eval(self.display_text))
            self.ids.equals_button.text = "OK"  # Change the equals button text to OK
        except Exception:
            self.display_text = "Error"

    def on_ok(self):
        self.ids.equals_button.text = "="  # Reset the button text to equals
        self.display_text = "0"
