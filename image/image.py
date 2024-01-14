from typing import Any
from PIL import Image as PILImage, ImageFilter, ImageEnhance
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as KivyImage
from kivy.properties import ObjectProperty, StringProperty
from io import BytesIO
import numpy as np



class ImagePreview(KivyImage):
    current_image = ObjectProperty(None)
    fit_mode = StringProperty('contain')
    original_image = ObjectProperty(None)
    def on_current_image(self, *_):
        self.texture_update()

    def texture_update(self, *largs):
        self._coreimage = self.current_image
        self._on_tex_change()
    
    def load_image(self, filename):
        self.original_image = PILImage.open(filename)
        self.current_image = self.pilimage_to_coreimage(self.original_image)

    def coreimage_to_pilimage(self):
        pil_image = PILImage.frombytes("RGBA",
                           self._coreimage.texture.size,
                           self._coreimage.texture.pixels)
        return pil_image
    
    def pilimage_to_coreimage(self, image):
        image_bytes = BytesIO()
        image.save(image_bytes, 'png')
        image_bytes.seek(0)
        return CoreImage(BytesIO(image_bytes.read()), ext='png')

    def blur(self, image, value):
        return image.filter(filter=ImageFilter.GaussianBlur(value))

    def brightness(self, image, value):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(value)

    def contrast(self, image, value):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(value)

    
    def update(self, tasks):
        # Update the image appying all the filter
        modifyable_image = self.original_image
        for key, value in tasks.items():
            func = getattr(self, str(key).lower())
            modifyable_image = func(modifyable_image, value)
        self.current_image = self.pilimage_to_coreimage(modifyable_image)


if __name__ == "__main__":
    image = PILImage.open("./assets/mina.jpeg")
    print(image.mode, image.size, image.format)
    # image.show()
    im = image.filter(ImageFilter.MinFilter(3))
    im.show()