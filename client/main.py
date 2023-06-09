# Client-side Application 

# Client Application

from kivymd.app import MDApp as App
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField as TextInput
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
import json


with open("client/settings.json","r") as f:
    data = json.load(f)
    font_path,title_font = data["font_path"],data["title_font"]

Window.size = (1080/3,2408/4)


class LoginPage(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1,1,1,1,mode="rgba")
            self.rect = Rectangle(pos=self.pos,size=self.size)
            self.bind(pos=self.update_rect,size=self.update_rect)
        self.app_title = Label(
            text = "MedEX",
            font_size=70,
            color=(0.19, 0.45, 1, 1),
            font_name=f"{font_path}/{title_font}",
            pos_hint={'center_x':0.5,'center_y':0.75}
        )
        self.user_input = TextInput(
            hint_text="Enter Username",
            helper_text="Forgor username?",
            pos_hint={'center_x':0.5,'center_y':0.55},
            size_hint_x=None,
            width=300
        )
        self.pass_input = TextInput(
            hint_text="Enter Password",
            helper_text="Forgor Password?",
            password=True,
            pos_hint={'center_x':0.5,'center_y':0.45},
            size_hint_x=None,
            width=300
        )
        self.loginbutton = MDRectangleFlatButton(
            text = "LOGIN",
            pos_hint={'center_x':0.35,'center_y':0.35}
        )
        self.skipbutton = MDRectangleFlatButton(
            text = "SKIP",
            pos_hint={'center_x':0.65,'center_y':0.35}
        )
        self.add_widget(self.app_title)
        self.add_widget(self.user_input)
        self.add_widget(self.pass_input)
        self.add_widget(self.loginbutton)
        self.add_widget(self.skipbutton)

    def update_rect(self,*args):
        self.rect.pos = self.pos 
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Change the primary color palette
        screen_manage = ScreenManager()
        login = LoginPage(name="login")
        screen_manage.add_widget(login)
        return screen_manage


app = MyApp()

if __name__ == '__main__':
    app.run()
