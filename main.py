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

# custom defined
from image.image import ImagePreview


Builder.load_file("mainpreview.kv")
Builder.load_file("toolpane.kv")

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Kivage(AnchorLayout):
    file_path = StringProperty('')
    file_name = StringProperty('')
    im = ObjectProperty()

    def __init__(self, **kwargs):
        self._trigger = Clock.create_trigger(self.update_image)
        super(Kivage, self).__init__(**kwargs)
        self.image = None
        self.pre_image = None
        self.test = 0
        self.image_data = BytesIO()
        self.kivy_image = KivyImage()
        self.bind(on_image=self._trigger)
        

        # helper
        self._prevous = None
        self._current = None
        self._holder = None

    def load_file(self):
        self.show_load()
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    
    def load(self, path, filename):
        self.file_path = path
        self.file_name = filename[0]
        im_widget = ImagePreview() 
        im_widget.load_image(filename[0])
        self.mainpreview.add_widget(im_widget)
        self.dismiss_popup()


class KivageApp(App):
    def build(self):
        self.title = "Photo Editor"
        self.icon = "assets/mina.jpeg"
        return Kivage()


if __name__ == '__main__':
    KivageApp().run()