# Client Application
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivymd.app import MDApp as App
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import MDScreenManager as ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField as TextInput
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
from kivymd.theming import ThemeManager
from kivymd.icon_definitions import md_icons
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivymd.uix.widget import MDWidget
from kivy_garden.mapview import MapView,MapMarkerPopup,MapMarker
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton,MDIconButton,MDFloatingActionButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import toolbar
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.transition import MDFadeSlideTransition,MDSwapTransition
from kivy.lang import Builder
import json
import websockets
import asyncio
import time
# The main function that will handle connection and communication
# with the server
# async def listen():
#     url = "ws://10.60.210.126:5000/client/ws"
#     # Connect to the server
#     async with websockets.connect(url) as ws:
#         time.sleep(10)
#         await ws.send(json.dumps({"event":"confirm","data":{"location":[12.33637695667677,76.6193388134931]}}))
#         # Stay alive forever, listening to incoming msgs
#         while True:
#             msg = await ws.recv()
#             print(msg)

# Start the connection
# asyncio.get_event_loop().run_until_complete(listen())


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
        self.loginbutton.bind(on_release=self.switchScreen)
        self.add_widget(self.app_title)
        self.add_widget(self.user_input)
        self.add_widget(self.pass_input)
        self.add_widget(self.loginbutton)
        self.add_widget(self.skipbutton)

    def update_rect(self,*args):
        self.rect.pos = self.pos 
        self.rect.size = self.size

    def switchScreen(self,*args):
            self.manager.transition = MDSwapTransition(
                duration=0.5
            )   
            self.manager.current = "emerg"


class Emergency(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical')
        self.gridlayout = MDGridLayout(rows=4)
        self.emergencyimage = Button(
            background_normal="client/assets/icons/emergencyamb.png",
            size_hint=(1,1)
            )
        self.options_button = MDFlatButton(
            text="Other Options",
            pos_hint={'center_x':0.5,'center_y':0},
            size_hint=(1,0.5)
        )
        self.emergencyimage.bind(on_press=self.switchScreen)
        self.gridlayout.add_widget(self.emergencyimage)
        self.gridlayout.add_widget(self.options_button)
        self.layout.add_widget(self.gridlayout)
        self.add_widget(self.layout)

    def switchScreen(self,*args):
        self.manager.transition = MDSwapTransition(
                duration=0.5
            )   
        self.manager.current = "map"
        

class Map(Screen):
    lat = 12.33637695667677
    lon = 76.6193388134931
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #Do Map Stuff
        self.map = MapView(zoom=17,size=(Window.width,Window.height), size_hint=(1,.7))
        self.map.center_on(self.lat,self.lon)
        self.pin = MapMarkerPopup(lat=self.lat,lon=self.lon)
        self.map.add_widget(self.pin)
        self.boxlayout = MDBoxLayout(orientation='vertical')
        self.gridlayout = MDGridLayout(rows=4,pos_hint={'center_y':0.5,'center_x':0.5}, size_hint=(1,.3))
        self.emergencybutton = MDIconButton(
            pos_hint={'center_x':0.5,'center_y':0.5},
            size_hint=(.5,.5),
            icon="phone-dial"
        )
        self.gridlayout.add_widget(self.emergencybutton)
        self.boxlayout.add_widget(self.map)
        self.boxlayout.add_widget(self.gridlayout)
        self.add_widget(self.boxlayout)

class MyApp(App):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Change the primary color palette
        screen_manage = ScreenManager()
        login = LoginPage(name="login")
        map = Map(name="map")
        emergency = Emergency(name="emerg")
        self.boxlayout = MDBoxLayout(orientation="vertical")
        screen_manage.add_widget(login)
        screen_manage.add_widget(map)
        screen_manage.add_widget(emergency)
        return screen_manage


app = MyApp()

if __name__ == '__main__':
    app.run()