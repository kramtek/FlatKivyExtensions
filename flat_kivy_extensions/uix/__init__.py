

from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

class CustomErrorContent(GridLayout):
    error_text = StringProperty('Default Error Text')


