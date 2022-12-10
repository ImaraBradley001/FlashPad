from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from tkinter import filedialog
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from tkinter import Tk, filedialog
import binascii

c = 0

Builder.load_file("style.kv")


class WelcomePage(Screen):
    pass


class MainPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_hex = False
        self.file = None
        self.saved = False
        self.file_is_open = False
        self.font_size = 15
        layout = FloatLayout()
        popupLabel = Label(text="Please save your work", pos_hint=({"center_x": .5, "center_y": .5}))
        layout.add_widget(popupLabel)
        self.popup = Popup(title='Reminder',
                           content=layout,
                           size_hint=(None, None),
                           size=(200, 100),
                           pos_hint=({"center_x": .5, "center_y": .9}))
        layout = FloatLayout()
        self.font_input = TextInput(pos_hint=({"center_x": .5, "center_y": .5}), multiline=False, size_hint=(1, .5))
        submit_button = Button(text="OK", pos_hint=({"center_x": .9, "center_y": .1}), size_hint=(.1, .1),
                               background_color=(30 / 255, 30 / 255, 30 / 255, 1), on_press=self.set_font_size)
        layout.add_widget(self.font_input)
        layout.add_widget(submit_button)
        self.popup2 = Popup(title='Enter Font Size',
                            content=layout,
                            size_hint=(None, None),
                            size=(200, 150),
                            pos_hint=({"center_x": .5, "center_y": .9}))
        self.previous = None

    def open_file(self):
        self.is_hex = False
        self.saved = False
        print("Opening file")
        root = Tk()
        root.withdraw()
        self.file = filedialog.askopenfilename()
        with open(self.file, "rb") as f:
            data = f.read()
        try:
            data = data.decode()
        except UnicodeDecodeError as e:
            print(e)
            return
        self.ids.file_content.text = data
        self.file_is_open = True

    def close_file(self):
        print("Closing file")
        if self.saved:
            self.ids.file_content.text = ""
        else:
            self.popup.open()

    def save_file(self):
        print("Saving file")
        if not self.file_is_open:
            root = Tk()
            root.withdraw()
            self.file = filedialog.askopenfilename()
        data = self.ids.file_content.text
        with open(self.file, "w") as f:
            f.write(data)
        self.saved = True

    def get_help(self):
        print("Getting help")

    def get_font_size(self):
        print("Setting font size")
        self.popup2.open()

    def set_font_size(self, i):
        self.popup2.dismiss()
        print("Setting font size")
        if self.font_input.text == "":
            return
        if self.font_input.text.isalpha():
            return
        if int(self.font_input.text) < 1:
            return
        print(self.font_input.text)
        self.ids.file_content.font_size = int(self.font_input.text)

    def string_to_hex(self):
        print("Converting to hex")
        if self.is_hex:
            self.hex_to_string()
            return
        hex_data = ''
        data = self.ids.file_content.text
        for char in data:
            ascii_int = ord(char)
            hex_char = hex(ascii_int)
            hex_data += hex_char+" "
        self.ids.file_content.text = hex_data
        self.is_hex = True
        self.ids.hex_button.text = "string"
        self.previous = data
        print(len(hex_data))

    def hex_to_string(self):
        print("Converting hex to string")
        print(self.previous)
        self.ids.file_content.text = self.previous
        self.is_hex = False
        self.ids.hex_button.text = "hex"

    def bytes_to_string(self):
        print("Converting bytes to string")

    def goto_settings(self):
        print("Going to settings")


class MainApp(MDApp):
    def build(self):
        from kivy.core.window import Window
        Window.size = (800, 600)
        Window.minimum_width, Window.minimum_height = Window.size
        self.sm = ScreenManager()
        self.sm.add_widget(WelcomePage(name='welcome_page'))
        self.sm.add_widget(MainPage(name='main_page'))
        Clock.schedule_interval(self.update, 1)
        return self.sm

    def update(self, i):
        global c
        if self.sm.current == "welcome_page":
            c += 1
            print(self.sm.current)
            if c == 2:
                self.sm.current = "main_page"
                c = 0


MainApp().run()
