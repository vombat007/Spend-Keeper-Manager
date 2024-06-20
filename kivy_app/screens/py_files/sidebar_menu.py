from kivy.uix.boxlayout import BoxLayout


class SidebarMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_sidebar(self):
        if self.x == 0:
            self.x = -self.width
        else:
            self.x = 0
