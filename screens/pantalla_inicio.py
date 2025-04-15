from kivy.lang import Builder
Builder.load_file("screens/home.kv")
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from  kivy.uix.stacklayout import StackLayout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def change_screen(self, screen_name):
        self.manager.current = screen_name