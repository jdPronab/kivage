from PIL import Image as PILImage, ImageFilter
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.properties import ObjectProperty, StringProperty
from io import BytesIO
import numpy as np
 
class ImagePreview(KivyImage):
    current_image = ObjectProperty(None)
    fit_mode = StringProperty('contain')
    
    def on_current_image(self, *_):
        self.texture_update()

    def texture_update(self, *largs):
        self._coreimage = self.current_image
        self._on_tex_change()
    
    def load_image(self, filename):
        loaded_image = PILImage.open(filename)
        image_bytes = BytesIO()
        loaded_image.save(image_bytes, format='jpeg')
        image_bytes.seek(0)
        self.current_image = CoreImage(BytesIO(image_bytes.read()), ext='jpg')

    def coreimage_to_pilimage(self):
        pil_image = PILImage.frombytes("RGB",
                           self._coreimage.texture.size,
                           self._coreimage.texture.pixels)
        return pil_image
    
    def blur(self):
        if self._coreimage:
            original_image = self.coreimage_to_pilimage()
            original_image.thumbnail(size=(500, 500))  #Resize image to make blur uniform and quicker
            blur_image = original_image.filter(filter=ImageFilter.GaussianBlur(4))
            image_bytes = BytesIO()
            blur_image.save(image_bytes, 'jpeg')
            image_bytes.seek(0)
            self.current_image = CoreImage(BytesIO(image_bytes.read()), ext='jpg')  #Save blurred image for easy toggle between original



if __name__ == "__main__":
    image = PILImage.open("./assets/mina.jpeg")
    print(image.mode, image.size, image.format)
    # image.show()
    im = image.filter(ImageFilter.MinFilter(3))
    im.show()