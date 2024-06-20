from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class HomeScreen(Screen):
    sidebar = ObjectProperty(None)

    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = None

    def set_token(self, token):
        self.token = token
        with open('token.txt', 'w') as token_file:
            token_file.write(token)

    def update_balance(self, balance, expenses, income):
        self.ids.balance_label.text = f'Main Balance: ${balance:.2f}'
        self.ids.expenses_label.text = f'Expenses: ${expenses:.2f}'
        self.ids.income_label.text = f'Income: ${income:.2f}'

    def toggle_sidebar(self):
        self.sidebar.toggle_sidebar()
