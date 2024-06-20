from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation


class SidebarMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_sidebar(self):
        if self.x == 0:
            anim = Animation(x=-self.width, duration=0.3)
        else:
            anim = Animation(x=0, duration=0.3)
        anim.start(self)