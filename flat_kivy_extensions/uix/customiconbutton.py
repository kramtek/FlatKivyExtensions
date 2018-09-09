
from kivy.metrics import dp

from kivy.properties import NumericProperty, StringProperty
from flat_kivy.uix.flaticonbutton import FlatIconButton

class CustomIconButton(FlatIconButton):
    icon_font_size = NumericProperty(5)
    orientation = StringProperty('lr-tb')
    pass

    def on_orientation(self, instance, value):
        if value.startswith('rl') or value.startswith('lr'):
            self._label.halign = 'left'
        else:
            self._label.halign = 'center'
            self._label.size_hint = (1.0, None)
            self._label.height = dp(25)

            self._icon.halign = 'center'
            self._icon.size_hint = (1.0, None)
            self._icon.height = dp(25)



