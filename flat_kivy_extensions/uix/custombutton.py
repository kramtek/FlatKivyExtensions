


from kivy.properties import NumericProperty
from kivy.uix.anchorlayout import AnchorLayout
from flat_kivy.uix.flatbutton import FlatButtonBase
from flat_kivy.uix.flaticonbutton import FlatIconButton

from flat_kivy.uix.behaviors import ButtonBehavior

class CustomButtonBase(FlatButtonBase):
    radius = NumericProperty(5)

class CustomButton(CustomButtonBase, ButtonBehavior, AnchorLayout):
    pass



