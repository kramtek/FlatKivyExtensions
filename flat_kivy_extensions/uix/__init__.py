

from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from flat_kivy.uix.behaviors import ThemeBehavior

class CustomPopupContent(GridLayout, ThemeBehavior):
    text = StringProperty('Default Error Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )
    messge_alignment = StringProperty('center')

class CustomBusyContent(GridLayout, ThemeBehavior):
    busy_text = StringProperty('Default Busy Text')
    label_color_tuple = ListProperty( ['Blue', '800'] )

    def __init__(self, cancel_callback=None, **kwargs):
        super(CustomBusyContent, self).__init__(**kwargs)


