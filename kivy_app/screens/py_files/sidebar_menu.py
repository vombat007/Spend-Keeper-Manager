from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import json


class SidebarMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_sidebar(self):
        if self.x == 0:
            anim = Animation(x=-self.width, duration=0.3)
        else:
            anim = Animation(x=0, duration=0.3)
        anim.start(self)

    def logout(self):
        def on_success(req, result):
            print(f"Logout successful: {result}")
            os.remove('tokens.json')
            app = App.get_running_app()
            app.sm.current = 'start'

        def on_failure(req, result):
            print(f"Logout failed: {result}")
            popup = Popup(title='Logout Failed',
                          content=Label(text='Could not log out. Please try again.'),
                          size_hint=(0.8, 0.2))
            popup.open()

        def on_error(req, error):
            print(f"Logout error: {error}")
            on_failure(req, error)

        if os.path.exists('tokens.json'):
            with open('tokens.json', 'r') as token_file:
                tokens = json.load(token_file)
                refresh_token = tokens.get('refresh')
                access_token = tokens.get('access')
                if refresh_token and access_token:
                    data = json.dumps({'refresh_token': refresh_token})
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {access_token}'
                    }
                    url = 'http://127.0.0.1:8000/api/logout/'
                    req = UrlRequest(url, req_body=data, req_headers=headers, on_success=on_success,
                                     on_failure=on_failure, on_error=on_error, method='POST')
                else:
                    print("Refresh token or access token not found in tokens.json")
                    on_failure(None, None)
        else:
            print("tokens.json file not found")
            on_failure(None, None)
