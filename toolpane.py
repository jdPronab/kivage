from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

class ToolPane(BoxLayout):
    blur_value = NumericProperty(0)
    brightness_value = NumericProperty(0)
    contrast_value = NumericProperty(0)

    def on_blur_value(self, *args):
        self.update()
    
    def on_brightness_value(self, *args):
        self.update()
    
    def on_contrast_value(self, *args):
        self.update()
    
    def update(self):
        tasks = {}
        for controller in self.controller.children:
            if controller.value != 0:
                tasks[controller.name] = controller.value
        self.kivyimage.mainpreview.children[0].update(tasks)

class SlideController(BoxLayout):
    name = StringProperty('')
    min = NumericProperty(0)
    max = NumericProperty(100)
    step = NumericProperty(1)
    value = NumericProperty(0)