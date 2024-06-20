from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.token = None

    def set_token(self, token):
        self.token = token
        # Save the token to local storage or some form of persistent storage
        with open('token.txt', 'w') as token_file:
            token_file.write(token)
        # Optionally, you can call some method here to update the home screen content
        # after setting the token.
        # self.update_home_screen()

    def update_balance(self, balance, expenses, income):
        self.ids.balance_label.text = f'Main Balance: ${balance:.2f}'
        self.ids.expenses_label.text = f'Expenses: ${expenses:.2f}'
        self.ids.income_label.text = f'Income: ${income:.2f}'
