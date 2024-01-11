from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


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
        super().__init__(**kwargs)
        self.image = None
        self.pre_image = None
        self.image_data = BytesIO()
        self.kivy_image = KivyImage()

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
        self.prepare_img()
        self.mainpreview.add_widget(self.kivy_image)
        self.dismiss_popup()

    def prepare_img(self):
        if self.file_name != '':
            self.pre_image = Image.open(self.file_name)
            self.image = self.pre_image
            self.update_image()
            
    def update_image(self):
        self.image.save(self.image_data, format='png')
        self.image_data.seek(0)
        self.image = CoreImage(BytesIO(self.image_data.read()), ext='png')
        self.kivy_image.texture = self.image.texture

class KivageApp(App):
    def build(self):
        self.title = "Photo Editor"
        self.icon = "assets/mina.jpeg"
        return Kivage()


if __name__ == '__main__':
    KivageApp().run()