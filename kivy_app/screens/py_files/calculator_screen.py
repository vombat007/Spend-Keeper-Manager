from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


class CalculatorScreen(Screen):
    operation_text = StringProperty("")
    result_text = StringProperty("0")

    def go_back(self, instance):
        self.reset_calculator()
        self.manager.current = 'transaction'

    def clear(self):
        self.reset_calculator()

    def half(self):
        if self.result_text and self.result_text != "Error":
            try:
                self.result_text = str(float(self.result_text) / 2)
                self.operation_text = self.result_text
            except ValueError:
                self.result_text = ""

    def percent(self):
        if self.result_text and self.result_text != "Error":
            try:
                self.result_text = str(float(self.result_text) / 100)
                self.operation_text = self.result_text
            except ValueError:
                self.result_text = ""

    def add_number(self, number):
        if self.operation_text == "0" or self.operation_text == "":
            self.operation_text = str(number)
        else:
            self.operation_text += str(number)
        self.update_result()

    def add_operator(self, operator):
        if self.operation_text and self.operation_text[-1] not in "+-*/":
            self.operation_text += operator
        self.update_result()

    def add_dot(self):
        if "." not in self.operation_text.split()[-1]:
            self.operation_text += "."
        self.update_result()

    def delete_last(self):
        if len(self.operation_text) > 1:
            self.operation_text = self.operation_text[:-1]
        else:
            self.operation_text = ""
        self.update_result()

    def calculate(self):
        try:
            self.result_text = str(eval(self.operation_text))
            self.ids.equals_button.text = "OK"
            self.ids.equals_button.bind(on_press=self.on_ok)  # Bind the on_ok method to the OK button
            self.ids.operation.height = 0
            self.ids.result.font_size = 100
            self.ids.result.height = '150dp'
        except Exception:
            self.result_text = ""

    def update_result(self):
        try:
            self.result_text = str(eval(self.operation_text))
        except Exception:
            self.result_text = ""

    def on_ok(self, instance):
        # Set the amount_input text on the transaction screen to the result
        self.manager.get_screen('transaction').ids.amount_input.text = self.result_text
        self.reset_calculator()
        self.manager.current = 'transaction'

    def reset_calculator(self):
        self.ids.equals_button.text = "="
        self.ids.equals_button.unbind(on_press=self.on_ok)  # Unbind the on_ok method from the OK button
        self.operation_text = ""
        self.result_text = "0"
        self.ids.operation.height = '50dp'
        self.ids.result.height = '75dp'
        self.ids.result.font_size = 50
        self.ids.result.opacity = 1
