
from kivy.properties import NumericProperty
from flat_kivy.uix.flaticonbutton import FlatIconButton

class CustomIconButton(FlatIconButton):
    icon_font_size = NumericProperty(5)
    pass


