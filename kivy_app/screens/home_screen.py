from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy_app.screens.sidebar_menu import SidebarMenu


class HomeScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Anchor layout for sidebar in the upper left corner
        anchor_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        self.sidebar_menu = SidebarMenu(screen_manager=screen_manager)
        anchor_layout.add_widget(self.sidebar_menu)

        layout.add_widget(anchor_layout)

        # Main content
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.balance_label = Label(text='Main Balance: $0.00', font_size=24)
        self.main_layout.add_widget(self.balance_label)

        self.expenses_label = Label(text='Expenses: $0.00', font_size=18)
        self.main_layout.add_widget(self.expenses_label)

        self.income_label = Label(text='Income: $0.00', font_size=18)
        self.main_layout.add_widget(self.income_label)

        layout.add_widget(self.main_layout)

        self.add_widget(layout)

    def update_balance(self, balance, expenses, income):
        self.balance_label.text = f'Main Balance: ${balance:.2f}'
        self.expenses_label.text = f'Expenses: ${expenses:.2f}'
        self.income_label.text = f'Income: ${income:.2f}'
