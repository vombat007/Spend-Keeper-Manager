from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os


class SplashScreen(Screen):
    def __init__(self, frame_rate=24, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add the first frame of the sequence
        self.img = Image(source='kivy_app/assets/img/frames/frame_0.png',
                         size_hint=(1, .5),
                         pos_hint={'center_x': .5, 'center_y': .5})
        layout.add_widget(self.img)
        self.add_widget(layout)

        # Schedule the transition to the home screen
        Clock.schedule_once(self.switch_to_home, 1)  # 3 seconds delay

        # Start the animation
        self.frames = [f'kivy_app/assets/img/frames/frame_{i}.png' for i in
                       range(len(os.listdir('kivy_app/assets/img/frames')))]
        self.current_frame = 0
        self.frame_rate = 1 / frame_rate  # frames per second
        Clock.schedule_interval(self.animate_logo, self.frame_rate)

    def animate_logo(self, dt):
        self.img.source = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def switch_to_home(self, dt):
        self.manager.current = 'home'
