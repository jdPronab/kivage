from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import numpy as np
import os

# custom defined
from settings import Primary
from image.image import ImagePreview


Builder.load_file("mainpreview.kv")
Builder.load_file("toolpane.kv")
Builder.load_file("style/filechooser.kv")

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Kivage(AnchorLayout):

    def load_file(self):
        self.show_load()
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file",
                            title_align='center',
                            title_color=Primary["text_color"],
                            content=content,
                            size_hint=(0.9, 0.9),
                            background_color=Primary["background_color"],
                            separator_color=Primary['green']
                            )
        self._popup.open()
    
    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", 
                            title_align='center',
                            title_color=Primary["text_color"],
                            content=content,
                            size_hint=(0.9, 0.9),
                            background_color=Primary["background_color"],
                            separator_color=Primary['green']
                            )
        self._popup.open()
    
    def load(self, path, filename):
        self.im_widget = ImagePreview() 
        self.im_widget.load_image(filename[0])
        if self.mainpreview.children:
            self.mainpreview.clear_widgets()
        self.mainpreview.add_widget(self.im_widget)
        self.dismiss_popup()
    
    def save(self, path, filename):
        fullpath = os.path.join(path, filename)
        fmt = filename.split('.')[1]
        fmt = str(fmt).upper()
        if fmt == 'JPG':
            fmt = 'JPEG'
        self.im_widget.save(fullpath, fmt)
        self.dismiss_popup()


class KivageApp(App):
    def build(self):
        self.title = "Photo Editor"
        self.icon = "assets/mina.jpeg"
        return Kivage()


if __name__ == '__main__':
    KivageApp().run()