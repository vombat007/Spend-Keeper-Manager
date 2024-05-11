from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class FinanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Text input for financial indicators
        self.financial_input = TextInput(hint_text='Enter financial indicators here...')
        layout.add_widget(self.financial_input)

        # Button to save
        save_button = Button(text='Save')
        save_button.bind(on_press=self.save_data)
        layout.add_widget(save_button)

        # Label to display saved data
        self.saved_data_label = Label(text='')
        layout.add_widget(self.saved_data_label)

        # Button to go back to home screen
        home_button = Button(text='Home')
        home_button.bind(on_press=self.go_to_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def save_data(self, instance):
        data = self.financial_input.text
        # Placeholder: Just display the saved data for now
        self.saved_data_label.text = f'Data saved: {data}'

    def go_to_home(self, instance):
        self.manager.current = 'home'
